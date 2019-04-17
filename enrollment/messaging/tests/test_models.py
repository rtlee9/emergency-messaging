import pytest
from django.conf import settings
from enrollment.messaging import models

pytestmark = pytest.mark.django_db


def test_message_get_absolute_url(message: models.Message):
    assert message.get_absolute_url() == f"/messages/{message.sid}/"


def test_message_str(message: models.Message):
    assert str(message.from_phone_number) in str(message)
    assert str(message.to_phone_number) in str(message)


def test_message_status_str(message_status: models.MessageStatus):
    assert str(message_status.datetime) in str(message_status)
    assert message_status.status in str(message_status)
