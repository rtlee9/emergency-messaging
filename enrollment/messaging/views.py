import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.urls import reverse

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from enrollment.students.models import Parent
from enrollment.messaging.models import Message, MessageStatus
from django.conf import settings

logger = logging.getLogger(__name__)
client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)


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
    # only hanlde POSt requests
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
    )
    message_in.save()

    # authenticate
    if not body.strip().startswith(settings.SMS_PIN):
        logger.warning(f'Incorect PIN for SID {sid}')
        MessageStatus(status='auth_fail', sid=sid).save()
        send_message(body="Incorrect PIN", to=from_number, callback=callback)
        return HttpResponse()
    else:
        clean_body = body[len(settings.SMS_PIN):]
        MessageStatus(status='auth_pass', sid=sid).save()
        resp = f"Your message has been sent: {clean_body}"

    # get all parent phone numbers
    parent_phone_numbers = Parent.objects.\
        values_list('phone_number', flat=True).\
        distinct('phone_number')
    logger.debug(parent_phone_numbers)

    for to_number in parent_phone_numbers:
        send_message(body=clean_body, to=to_number, callback=callback)

    # send message and return empty response
    send_message(body=resp, to=from_number, callback=callback)
    return HttpResponse()


def send_message(body, to, callback=None):
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
    )
    message_out.save()
