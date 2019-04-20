import pytest
from django.conf import settings
from django.test import RequestFactory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
import pytest

from enrollment.students import views, models
from enrollment.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestParentListView:

    @pytest.fixture(autouse=True)
    def setUp(self, request_factory: RequestFactory):
        self.view = views.ParentListView.as_view()
        self.request = request_factory.get("/parents/")

    def test_not_staff(self, user: UserFactory):
        self.request.user = user
        with pytest.raises(PermissionDenied) as exp:
            response = self.view(self.request)
            assert 'access required' in str(exp.value)

    def test_anonymous_user(self):
        self.request.user = AnonymousUser()
        response = self.view(self.request)
        assert response.status_code == 302
        assert 'login' in response.url

    def test_user_staff(self, user: UserFactory):
        user.is_staff = True
        self.request.user = user
        response = self.view(self.request)
        assert response.status_code == 200
