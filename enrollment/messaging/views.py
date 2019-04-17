import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaulttags import register

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import pytz
from datetime import datetime as dt

from enrollment.students.models import Parent
from enrollment.messaging.models import Message, MessageStatus
from enrollment.users.mixins import StaffRequiredMixin
from django.conf import settings

logger = logging.getLogger(__name__)
client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class MessageListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(msg_type=Message.INBOUND)


class MessageDetailView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = MessageStatus
    template_name = 'messaging/message_detail.html'

    def get_queryset(self):
        sid = self.kwargs['sid']
        return MessageStatus.objects.filter(sid=sid)

    def get_context_data(self):
        context = super().get_context_data()
        context['message_object'] = Message.objects.\
            get(sid=self.kwargs['sid'])
        context['latest_status'] = self.get_queryset().latest()
        context['children_messages'] = Message.objects.\
            filter(parent_id=self.kwargs['sid'])
        children_statuses = MessageStatus.objects.\
            filter(sid__in=context['children_messages'].values_list('sid', flat=True)).\
            order_by('sid', '-datetime').\
            distinct('sid')
        context['children_statuses'] = {
            status.sid: status
            for status in children_statuses
        }
        return context


@csrf_exempt
def sms_status(request):
    # handlle request
    logger.debug(request.POST)
    sid, status = request.POST.get('MessageSid'), request.POST.get('MessageStatus')
    logger.info(f'Message {sid} {status}')

    # add status object
    message_status = MessageStatus(
        status=status,
        sid=sid,
    )
    message_status.save()
    return HttpResponse()


@csrf_exempt
def sms_response(request):
    # only hanlde POST requests
    logger.debug(request.POST)
    if request.method != 'POST':
        return HttpResponse(f'{request.method} request not supported', status=405)

    # parse message
    from_number = request.POST.get('From')
    to_number = request.POST.get('To')
    body = request.POST.get('Body')
    sid = request.POST.get('MessageSid')
    status = request.POST.get('SmsStatus')
    callback = request.build_absolute_uri(reverse('messaging:sms-status'))

    # handle errors
    if not from_number:
        return HttpResponse(f'Missing From phone number', status=400)
    if not to_number:
        return HttpResponse(f'Missing To phone number', status=400)
    if not sid:
        return HttpResponse(f'Missing SID', status=400)
    if not status:
        return HttpResponse(f'Missing SMS status', status=400)

    MessageStatus(status=status, sid=sid).save()

    # create message object for persistence
    message_in = Message(
        sid=sid,
        body=body,
        from_phone_number=from_number,
        to_phone_number=to_number,
        msg_type=Message.INBOUND,
    )
    message_in.save()

    # if recently authenticated then can skip auth this time
    msgs = Message.objects.\
        filter(from_phone_number=from_number).\
        values_list('sid', flat=True)
    try:
        last_pass = MessageStatus.objects.\
            filter(sid__in=msgs, status=MessageStatus.AUTH_PASS).\
            latest()
        logger.debug(f'Last successfal authentication: {last_pass}')
        last_pass = last_pass.datetime
        now = dt.utcnow().replace(tzinfo=pytz.utc)
        delta = now - last_pass
        auth_required = delta.seconds > settings.AUTH_SECONDS
        if auth_required:
            logger.debug(f'{delta.seconds:,.0f} seconds since last successfull authentication.')
        else:
            logger.info(f'Skipping authentication: {delta.seconds:,.0f} seconds since last successfull authentication.')
            MessageStatus(status=MessageStatus.AUTH_SKIP, sid=sid).save()
    except MessageStatus.DoesNotExist:
        logger.info('No previous successfull authentications (auth required)')
        auth_required = True

    # authenticate
    if auth_required and not body.strip().startswith(settings.SMS_PIN):
        logger.warning(f'Incorect PIN for SID {sid}')
        MessageStatus(status=MessageStatus.AUTH_FAIL, sid=sid).save()
        send_message(
            body="Incorrect PIN",
            to=from_number,
            callback=callback,
            parent=message_in,
            msg_type=MessageStatus.AUTH_FAIL,
        )
        return HttpResponse()
    else:
        clean_body = body[len(settings.SMS_PIN):]
        if auth_required:
            MessageStatus(status=MessageStatus.AUTH_PASS, sid=sid).save()
        resp = f"Your message has been sent: {clean_body}"

    # get all parent phone numbers
    parent_phone_numbers = Parent.objects.\
        values_list('phone_number', flat=True).\
        distinct('phone_number')

    for to_number in parent_phone_numbers:
        send_message(
            body=clean_body,
            to=to_number,
            callback=callback,
            parent=message_in,
        )

    # send message and return empty response
    send_message(
        body=resp,
        to=from_number,
        callback=callback,
        parent=message_in,
        msg_type=Message.CONFIRMATION,
    )
    return HttpResponse()


def send_message(body, to, callback=None, parent=None, msg_type=Message.OUTBOUND):
    twilio_message = client.messages.create(
        body=body,
        from_=settings.TWILIO_NUMBER,
        to=to,
        status_callback=callback,
    )
    logger.info(f'Twilio message to {to} SID {twilio_message.sid}')
    message_out = Message(
        from_phone_number=settings.TWILIO_NUMBER,
        to_phone_number=to,
        body=body,
        sid=twilio_message.sid,
        parent=parent,
        msg_type=msg_type,
    )
    message_out.save()
