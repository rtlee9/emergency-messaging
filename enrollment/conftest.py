import pytest
from django.conf import settings
from django.test import RequestFactory

from enrollment.users.tests.factories import UserFactory
from enrollment.messaging.tests.factories import MessageFactory, MessageStatusFactory
from enrollment.students.tests.factories import ParentFactory, SiteFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def message() -> MessageFactory:
    return MessageFactory()


@pytest.fixture
def message_status() -> MessageStatusFactory:
    return MessageStatusFactory()


@pytest.fixture
def parent() -> ParentFactory:
    return ParentFactory()


@pytest.fixture
def student() -> StudentFactory:
    return StudentFactory()


@pytest.fixture
def site() -> SiteFactory:
    return SiteFactory()


@pytest.fixture
def classroom() -> ClassroomFactory:
    return ClassroomFactory()
