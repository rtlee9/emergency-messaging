import pytest
from django.conf import settings
from django.urls import reverse, resolve

from enrollment.students import models

pytestmark = pytest.mark.django_db


def test_parent_detail(parent: models.Parent):
    assert reverse("students:parent-detail", kwargs={"pk": parent.pk}) == f"/parents/{parent.pk}/"
    assert resolve(f"/parents/{parent.pk}/").view_name == "students:parent-detail"


def test_list():
    assert reverse("students:parent-list") == "/parents/"
    assert resolve("/parents/").view_name == "students:parent-list"


def test_update(parent: models.Parent):
    assert reverse("students:parent-update", kwargs={'pk': parent.pk}) == f"/parents/{parent.pk}/update/"
    assert "students:parent-update" == resolve(f"/parents/{parent.pk}/update/").view_name


def test_delete(parent: models.Parent):
    assert reverse("students:parent-delete", kwargs={'pk': parent.pk}) == f"/parents/{parent.pk}/delete/"
    assert "students:parent-delete" == resolve(f"/parents/{parent.pk}/delete/").view_name


def test_add(parent: models.Parent):
    assert reverse("students:parent-add") == f"/parents/add/"
    assert "students:parent-add" == resolve(f"/parents/add/").view_name
