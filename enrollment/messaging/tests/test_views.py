import pytest
from django.conf import settings
from django.test import RequestFactory
from random import randint
import phonenumbers
import time

from enrollment.messaging import views, models
from enrollment.students.tests.factories import ParentFactory
from enrollment.students.models import Parent
from .factories import MessageFactory

pytestmark = pytest.mark.django_db


class TwilioTestClient:

    def __init__(self, sid, token):
        self.sid = sid
        self.token = token
        self.messages = TwillioTestClientMessages()


class TwillioTestClientMessages:

    def __init__(self):
        self.created = []

    def create(self, to, from_, body, status_callback=None):
        self.created.append({
            'to': to,
            'from_': from_,
            'body': body,
            'status_callback': status_callback,
        })
        return TwilioTestMessage(
            body=body,
            from_phone_number=from_,
            to_phone_number=to,
        )


class TwilioTestMessage(object):

    def __init__(self, *args, **kwargs):
        message = MessageFactory(*args, **kwargs)
        self.sid = message.sid


class TestSmsView:

    @classmethod
    def _construct_data(cls, message):
        return {
            'From': message.from_phone_number,
            'To': message.to_phone_number,
            'Body': message.body,
            'MessageSid': message.sid,
            'SmsStatus': models.MessageStatus.TWILIO_SENT,
        }

    @classmethod
    def _test_empty_response(cls, response):
        assert response.status_code == 200
        assert not response.content

    @pytest.fixture(autouse=True)
    def setup(self):
        self.view = views.sms_response
        views.client = TwilioTestClient(
            settings.TWILIO_SID, settings.TWILIO_TOKEN)

    def test_no_pin(
        self,
        message: models.Message,
        message_status: models.MessageStatus,
        request_factory: RequestFactory,
    ):
        request = request_factory.post(
            "/sms/", self._construct_data(message))
        response = self.view(request)
        # expecting empty repsone
        assert response.status_code == 200
        assert not response.content
        # check test client for message
        msgs = views.client.messages.created
        assert len(msgs) == 1
        assert msgs[0]['to'] == message.from_phone_number
        assert msgs[0]['body'] == 'Incorrect PIN'

    def test_no_from_number(
        self,
        message: models.Message,
        message_status: models.MessageStatus,
        request_factory: RequestFactory,
    ):
        data = self._construct_data(message)
        data.pop('From')
        request = request_factory.post("/sms/", data)
        response = self.view(request)
        assert response.status_code == 400
        assert 'phone number' in str(response.content).lower()

    def test_get_request(
        self,
        message: models.Message,
        message_status: models.MessageStatus,
        request_factory: RequestFactory,
    ):
        request = request_factory.get("/sms/")
        response = self.view(request)
        assert response.status_code == 405
        assert 'not supported' in str(response.content).lower()

    def test_good_message(
        self,
        message: models.Message,
        message_status: models.MessageStatus,
        request_factory: RequestFactory,
    ):
        msg_og = message.body
        msg_og_trunc = msg_og[:-len(settings.SMS_PIN)]
        message.body = settings.SMS_PIN + msg_og_trunc

        # create batch of parents
        n = randint(2, 10)
        parents = ParentFactory.create_batch(size=n)

        # send request
        request = request_factory.post(
            "/sms/", self._construct_data(message))
        response = self.view(request)
        self._test_empty_response(response)

        # check test client for confirmation message
        msgs = views.client.messages.created
        assert len(msgs) == 1 + n
        # last message is confirmation
        assert msgs[-1]['to'] == phonenumbers.format_number(
            message.from_phone_number, phonenumbers.PhoneNumberFormat.E164)
        assert msgs[-1]['body'].lower().startswith('your message has been sent')
        # check messages to all parents
        for i in range(n - 1):
            msg = msgs[i]
            parent = Parent.objects.get(phone_number=msg['to'])
            assert msg['body'] == msg_og_trunc
            assert msg['to'] == phonenumbers.format_number(
                parent.phone_number, phonenumbers.PhoneNumberFormat.E164)

        # subsequent request shouldn't require PIN
        message.body = msg_og
        request = request_factory.post(
            "/sms/", self._construct_data(message))
        response = self.view(request)
        self._test_empty_response(response)
        # check test client for confirmation message
        msgs = views.client.messages.created
        assert len(msgs) == 2 * (1 + n)
        # last message is confirmation
        assert msgs[-1]['to'] == phonenumbers.format_number(
            message.from_phone_number, phonenumbers.PhoneNumberFormat.E164)
        assert msgs[-1]['body'].lower().startswith('your message has been sent')
        # check messages to all parents
        for i in range(n + 2, 2 * (1 + n) - 1):
            msg = msgs[i]
            parent = Parent.objects.get(phone_number=msg['to'])
            assert msg['body'] == msg_og
            assert msg['to'] == phonenumbers.format_number(
                parent.phone_number, phonenumbers.PhoneNumberFormat.E164)

        # subsequent request should require PIN if after timeout
        time.sleep(settings.AUTH_SECONDS + 1)
        message.body = msg_og
        request = request_factory.post(
            "/sms/", self._construct_data(message))
        response = self.view(request)
        self._test_empty_response(response)
        # check test client for confirmation message
        msgs = views.client.messages.created
        assert len(msgs) == 2 * (1 + n) + 1
        # last message is confirmation
        assert msgs[-1]['to'] == message.from_phone_number
        assert msgs[-1]['body'] == 'Incorrect PIN'
