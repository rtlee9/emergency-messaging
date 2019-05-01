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
        self.view = self.view_class.as_view()
        self.request = request_factory.get(f"/{self.url_path}/")
        self.client = Client()

    def make_request(self, request):
        return self.view(request)

    def test_not_staff(self, user: UserFactory):
        self.request.user = user
        with pytest.raises(PermissionDenied) as exp:
            response = self.make_request(self.request)
            assert 'access required' in str(exp.value)

    def test_anonymous_user(self):
        self.request.user = AnonymousUser()
        response = self.make_request(self.request)
        assert response.status_code == 302
        assert 'login' in response.url

    def test_user_staff(self, user: UserFactory):
        user.is_staff = True
        self.request.user = user
        assert self.make_request(self.request).status_code == 200


class BaseTestPkView(BaseTestView):
    """Handles pk based requests."""

    def make_request(self, request):
        return self.view(request, pk=self.factory().pk)


class BaseTestParentView(BaseTestView):
    """Base class for Parent views."""
    factory = factories.ParentFactory
    url_path = 'parents'


class TestParentViewList(BaseTestParentView):
    view_class = views.ParentListView


class TestParentViewCreate(BaseTestParentView):
    view_class = views.ParentCreate


class TestParentViewDetail(BaseTestParentView, BaseTestPkView):
    view_class = views.ParentDetailView


class TestParentViewDelete(BaseTestParentView, BaseTestPkView):
    view_class = views.ParentDelete


class BaseTestClassroomView(BaseTestView):
    """Base class for Classroom views."""
    view_class = views.ClassroomListView
    factory = factories.ClassroomFactory
    url_path = 'classroom'


class TestClassroomViewList(BaseTestClassroomView):
    view_class = views.ClassroomListView


class TestClassroomViewCreate(BaseTestClassroomView):
    view_class = views.ClassroomCreate


class TestClassroomViewDetail(BaseTestClassroomView, BaseTestPkView):
    view_class = views.ClassroomDetailView


class TestClassroomViewDelete(BaseTestClassroomView, BaseTestPkView):
    view_class = views.ClassroomDelete


class BaseTestStudentView(BaseTestView):
    """Base class for Student views."""
    factory = factories.StudentFactory
    url_path = 'students'


class TestStudentViewList(BaseTestStudentView):
    view_class = views.StudentListView


class TestStudentViewCreate(BaseTestStudentView):
    view_class = views.StudentCreate


class TestStudentViewDetail(BaseTestStudentView, BaseTestPkView):
    view_class = views.StudentDetailView


class TestStudentViewDelete(BaseTestStudentView, BaseTestPkView):
    view_class = views.StudentDelete


class BaseTestSiteView(BaseTestView):
    """Base class for Student views."""
    factory = factories.SiteFactory
    url_path = 'sites'


class TestSiteViewList(BaseTestSiteView):
    view_class = views.SiteListView


class TestSiteViewCreate(BaseTestSiteView):
    view_class = views.SiteCreate


class TestSiteViewDetail(BaseTestSiteView, BaseTestPkView):
    view_class = views.SiteDetailView


class TestSiteViewDelete(BaseTestSiteView, BaseTestPkView):
    view_class = views.SiteDelete
