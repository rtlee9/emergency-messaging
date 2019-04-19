import pytest
from django.conf import settings
from django.urls import reverse, resolve

from enrollment.students import models

pytestmark = pytest.mark.django_db


def test_parent_detail(parent: models.Parent):
    assert (
        reverse("students:parent-detail", kwargs={"pk": parent.pk})
        == f"/parents/{parent.pk}/"
    )
    assert resolve(f"/parents/{parent.pk}/").view_name == "students:parent-detail"


def test_list():
    assert reverse("students:parent-list") == "/parents/"
    assert resolve("/parents/").view_name == "students:parent-list"
