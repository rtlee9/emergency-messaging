import pytest
from django.conf import settings
from django.urls import reverse, resolve

from enrollment.messaging import models

pytestmark = pytest.mark.django_db


def test_message_detail(message: models.Message):
    assert (
        reverse("messaging:message-detail", kwargs={"sid": message.sid})
        == f"/messages/{message.sid}/"
    )
    assert resolve(f"/messages/{message.sid}/").view_name == "messaging:message-detail"


def test_list():
    assert reverse("messaging:message-list") == "/messages/"
    assert resolve("/messages/").view_name == "messaging:message-list"


def test_sms():
    assert reverse("messaging:sms") == "/sms/"
    assert resolve("/sms/").view_name == "messaging:sms"


def test_sms_status():
    assert reverse("messaging:sms-status") == "/sms/status/"
    assert resolve("/sms/status/").view_name == "messaging:sms-status"
