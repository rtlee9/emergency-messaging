import pytest
from django.conf import settings
from django.test import RequestFactory
from random import randint, choice
import phonenumbers
import time

from enrollment.messaging import views, models
from enrollment.students.tests.factories import ParentFactory, SiteFactory, StudentFactory, ClassroomFactory
from enrollment.students.models import Parent, Student, Classroom, Site
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
        message = TwilioTestMessage(
            body=body,
            from_phone_number=from_,
            to_phone_number=to,
        )
        # TODO: make callback
        # TEMP: add statuses
        message_status = models.MessageStatus(status=models.MessageStatus.TWILIO_SENT, sid=message.sid).save()
        message_status = models.MessageStatus(status=models.MessageStatus.TWILIO_DELIVERED, sid=message.sid).save()
        return message


class TwilioTestMessage(object):

    def __init__(self, *args, **kwargs):
        message = MessageFactory(*args, **kwargs)
        self.sid = message.sid


class TestSmsView:
    ns = 3
    nc = 20
    np = 40

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
        self.sites = SiteFactory.create_batch(self.ns)
        self.classrooms = ClassroomFactory.create_batch(self.nc)
        self.parents = self._gen_all_families()

    def teardown(self):
        Site.objects.all().delete()
        Classroom.objects.all().delete()
        Parent.objects.all().delete()
        Student.objects.all().delete()

    def test_no_pin(
        self,
        message: models.Message,
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
        request_factory: RequestFactory,
    ):
        request = request_factory.get("/sms/")
        response = self.view(request)
        assert response.status_code == 405
        assert 'not supported' in str(response.content).lower()

    def _gen_family(self, num_parents=2):
        """Generate a family of num_parents with an arbitrary number of students.
        """
        parents = []
        # add two parents who share ns students
        num_students = randint(2, 4)
        students = StudentFactory.create_batch(size=num_students)
        for _ in range(2):
            parents.append(ParentFactory(students=students))
        return parents

    def _gen_all_families(self):
        # create batch of parents
        parents = self._gen_family()
        parents.extend(self._gen_family())
        parents.extend(self._gen_family(1))
        parents.extend(self._gen_family(3))
        return parents

    def clear_client(fn):
        def wrapper(*args, **kwargs):
            response = fn(*args, **kwargs)
            views.client.messages.created = []
            return response
        return wrapper

    @clear_client
    def _check_parse_site(self):
        """Check site prompt and respond with random selection."""
        msgs = views.client.messages.created
        # check twilio test client sent the right message
        assert len(msgs) == 1
        assert msgs[0]['body'].startswith('Please select a site')
        assert len(msgs[0]['body'].split('\n')) == self.ns + 1
        # parse site options
        site_options = [
            full_option.split(':')[0][1:-1]
            for full_option
            in msgs[0]['body'].split('\n')[1:]
        ]
        site_choice = choice(site_options)
        return site_choice

    @clear_client
    def _test_distribution(self, site_choice, from_phone_number, expected_msg):
        """Check test client for confirmation message."""
        msgs = views.client.messages.created
        n = Parent.objects.\
            filter(students__classroom__site__pk=int(site_choice)).\
            distinct().count()
        assert len(msgs) == 1 + n
        # last message is confirmation
        assert msgs[-1]['to'] == phonenumbers.format_number(
            from_phone_number, phonenumbers.PhoneNumberFormat.E164)
        assert msgs[-1]['body'].lower().startswith('your message has been sent')
        # check messages to all parents
        for i in range(n - 1):
            msg = msgs[i]
            parent = Parent.objects.get(phone_number=msg['to'])
            assert msg['body'] == expected_msg
            assert msg['to'] == phonenumbers.format_number(
                parent.phone_number, phonenumbers.PhoneNumberFormat.E164)

    def _handle_respond_site_prompt(self, from_phone_number, request_factory, site_choice=None):
        if site_choice:
            _ = self._check_parse_site()
        else:
            site_choice = self._check_parse_site()
        prompt_response = MessageFactory(
            body=f'{site_choice}',
            from_phone_number=from_phone_number,
        )
        request = request_factory.post(
            "/sms/", self._construct_data(prompt_response))
        response = self.view(request)
        self._test_empty_response(response)
        return site_choice

    def _request_check_empty(self, message, request_factory):
        """Send message as POST request, assert empty response."""
        request = request_factory.post(
            "/sms/", self._construct_data(message))
        response = self.view(request)
        self._test_empty_response(response)

    @clear_client
    def _test_pin_timeout(self, from_phone_number, request_factory):
        """Test PIN timeout. Expecting a SMS response indicating incorrect PIN."""
        msgs = views.client.messages.created
        time.sleep(settings.AUTH_SECONDS + 1)
        message = MessageFactory(from_phone_number=from_phone_number)
        self._request_check_empty(message, request_factory)
        # check test client for confirmation message
        msgs = views.client.messages.created
        assert len(msgs) == 1
        assert msgs[-1]['to'] == message.from_phone_number
        assert msgs[-1]['body'] == 'Incorrect PIN'

    def test_good_message(
        self,
        message: models.Message,
        request_factory: RequestFactory,
    ):
        # construct message with PIN
        msg_og = message.body
        msg_og_trunc = msg_og[:-len(settings.SMS_PIN)]
        message.body = settings.SMS_PIN + msg_og_trunc
        from_phone_number = message.from_phone_number

        # check site prompt, choose arbitrary site, confirm distribution
        self._request_check_empty(message, request_factory)
        site_choice = self._handle_respond_site_prompt(from_phone_number, request_factory)
        self._test_distribution(site_choice, from_phone_number, msg_og_trunc)
        return from_phone_number

    def test_subsequent_requst(
        self,
        message: models.Message,
        request_factory: RequestFactory,
    ):
        # subsequent request shouldn't require PIN
        from_phone_number = self.test_good_message(message, request_factory)
        message = MessageFactory(from_phone_number=from_phone_number)
        self._request_check_empty(message, request_factory)
        site_choice = self._handle_respond_site_prompt(from_phone_number, request_factory)
        self._test_distribution(site_choice, from_phone_number, message.body)

    @clear_client
    def _test_bad_group_selection(
            self,
            message: models.Message,
            request_factory: RequestFactory,
            site_choice: str,
            expected_response: str,
    ):
        # check site prompt, choose bad site, confirm error handling
        from_phone_number = self.test_good_message(message, request_factory)
        self._request_check_empty(message, request_factory)
        site_choice = self._handle_respond_site_prompt(
            from_phone_number, request_factory, site_choice=site_choice)
        msgs = views.client.messages.created
        assert len(msgs) == 1
        assert msgs[-1]['to'] == message.from_phone_number
        assert expected_response.lower() in msgs[-1]['body'].lower()

    def test_bad_group_selection_char(
            self,
            message: models.Message,
            request_factory: RequestFactory,
    ):
        self._test_bad_group_selection(message, request_factory, 'a', 'must be an integer')

    def test_bad_group_selection_str(
            self,
            message: models.Message,
            request_factory: RequestFactory,
    ):
        self._test_bad_group_selection(message, request_factory, message.body, 'must be an integer')

    def test_bad_group_selection_negative_int(
            self,
            message: models.Message,
            request_factory: RequestFactory,
    ):
        self._test_bad_group_selection(message, request_factory, -1, 'no students found')

    def test_bad_group_selection_large_float(
            self,
            message: models.Message,
            request_factory: RequestFactory,
    ):
        self._test_bad_group_selection(message, request_factory, 10e6, 'must be an integer')

    def test_bad_group_selection_large_int(
            self,
            message: models.Message,
            request_factory: RequestFactory,
    ):
        self._test_bad_group_selection(message, request_factory, 1000, 'no students found')

    @pytest.mark.slow
    def test_pin_timeout(
        self,
        message: models.Message,
        request_factory: RequestFactory,
    ):
        # subsequent request should require PIN if after timeout
        from_phone_number = self.test_good_message(message, request_factory)
        self._test_pin_timeout(from_phone_number, request_factory)
