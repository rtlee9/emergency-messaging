import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from enrollment.students.models import Parent
from enrollment.messaging.models import Message, MessageStatus
from enrollment.messaging import account_sid, auth_token, pin, twilio_number

logger = logging.getLogger(__name__)
client = Client(account_sid, auth_token)

if pin is None:
    logger.error('No SMS PIN is set')


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
    message_status = MessageStatus(status=status, sid=sid)
    message_status.save()

    # handle errors
    if not from_number:
        return HttpResponse(f'Missing From phone number', status=400)
    if not to_number:
        return HttpResponse(f'Missing To phone number', status=400)

    # map phone numbers to parents
    try:
        from_parent = Parent.objects.get(phone_number=from_number)
    except Parent.DoesNotExist:
        logger.warning(f'Parent not found for phone number {from_number}')
        from_parent = None
    try:
        to_parent = Parent.objects.get(phone_number=to_number)
    except Parent.DoesNotExist:
        logger.warning(f'Parent not found for phone number {to_number}')
        to_parent = None

    # create message object for persistence
    message_in = Message(
        sid=sid,
        body=body,
        from_phone_number=from_number,
        to_phone_number=to_number,
        from_parent=from_parent,
        to_parent=to_parent,
    )
    message_in.save()

    # authenticate
    if not body.strip().startswith(pin):
        logger.warning('Incorect PIN')
        logger.warning(body)
        send_message(body="Incorrect PIN", to=from_number)
        return HttpResponse()
    else:
        clean_body = body[len(pin):]
        resp = f"Your message has been sent: {clean_body}"

    # get all parent phone numbers
    parent_phone_numbers = Parent.objects.\
        values_list('phone_number', flat=True).\
        distinct('phone_number')
    logger.debug(parent_phone_numbers)

    for to_number in parent_phone_numbers:
        send_message(body=clean_body, to=to_number)

    send_message(body=resp, to=from_number)
    return HttpResponse()


def send_message(body, to):
    twilio_message = client.messages.create(
        body=body,
        from_=twilio_number,
        to=to,
        status_callback='http://7cb8eb62.ngrok.io/sms/status',
    )
    logger.debug(f'Twilio message to {to} SID {twilio_message.sid}')
    message_out = Message(
        from_phone_number=twilio_number,
        to_phone_number=to,
        body=body,
        sid=twilio_message.sid,
    )
    message_out.save()
