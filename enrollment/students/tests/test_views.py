import pytest
from django.conf import settings
from django.test import RequestFactory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import Client
import pytest

from enrollment.students import views, models
from enrollment.users.tests.factories import UserFactory
from enrollment.students.tests import factories

pytestmark = pytest.mark.django_db


class BaseTestView:

    @pytest.fixture(autouse=True)
    def setUp(self, request_factory: RequestFactory):
        self.list_view = self.list_view.as_view()
        self.detail_view = self.detail_view.as_view()
        self.request = request_factory.get(f"/{self.url_path}/")
        self.client = Client()

    def test_not_staff(self, user: UserFactory):
        self.request.user = user
        with pytest.raises(PermissionDenied) as exp:
            response = self.list_view(self.request)
            assert 'access required' in str(exp.value)

    def test_anonymous_user(self):
        self.request.user = AnonymousUser()
        response = self.list_view(self.request)
        assert response.status_code == 302
        assert 'login' in response.url

    def test_user_staff(self, user: UserFactory):
        user.is_staff = True
        self.request.user = user
        assert self.list_view(self.request).status_code == 200
        assert self.detail_view(self.request, pk=self.factory().pk).status_code == 200


class TestParentView(BaseTestView):
    factory = factories.ParentFactory
    list_view = views.ParentListView
    detail_view = views.ParentDetailView
    url_path = 'parents'


class TestClassroomView(BaseTestView):
    factory = factories.ClassroomFactory
    list_view = views.ClassroomListView
    detail_view = views.ClassroomDetailView
    url_path = 'classroom'


class TestStudentView(BaseTestView):
    factory = factories.StudentFactory
    list_view = views.StudentListView
    detail_view = views.StudentDetailView
    url_path = 'students'


class TestSiteView(BaseTestView):
    factory = factories.SiteFactory
    list_view = views.SiteListView
    detail_view = views.SiteDetailView
    url_path = 'sites'
