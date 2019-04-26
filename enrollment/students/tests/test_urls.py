import pytest
from django.conf import settings
from django.urls import reverse, resolve

from enrollment.students import models

pytestmark = pytest.mark.django_db


def test_parent_detail(parent: models.Parent):
    assert reverse("students:parent-detail", kwargs={"pk": parent.pk}) == f"/parents/{parent.pk}/"
    assert resolve(f"/parents/{parent.pk}/").view_name == "students:parent-detail"


def test_parent_list():
    assert reverse("students:parent-list") == "/parents/"
    assert resolve("/parents/").view_name == "students:parent-list"


def test_parent_update(parent: models.Parent):
    assert reverse("students:parent-update", kwargs={'pk': parent.pk}) == f"/parents/{parent.pk}/update/"
    assert "students:parent-update" == resolve(f"/parents/{parent.pk}/update/").view_name


def test_parent_delete(parent: models.Parent):
    assert reverse("students:parent-delete", kwargs={'pk': parent.pk}) == f"/parents/{parent.pk}/delete/"
    assert "students:parent-delete" == resolve(f"/parents/{parent.pk}/delete/").view_name


def test_parent_add(parent: models.Parent):
    assert reverse("students:parent-add") == f"/parents/add/"
    assert "students:parent-add" == resolve(f"/parents/add/").view_name


def test_site_detail(site: models.Site):
    assert reverse("students:site-detail", kwargs={"pk": site.pk}) == f"/sites/{site.pk}/"
    assert resolve(f"/sites/{site.pk}/").view_name == "students:site-detail"


def test_site_list():
    assert reverse("students:site-list") == "/sites/"
    assert resolve("/sites/").view_name == "students:site-list"


def test_site_update(site: models.Site):
    assert reverse("students:site-update", kwargs={'pk': site.pk}) == f"/sites/{site.pk}/update/"
    assert "students:site-update" == resolve(f"/sites/{site.pk}/update/").view_name


def test_site_delete(site: models.Site):
    assert reverse("students:site-delete", kwargs={'pk': site.pk}) == f"/sites/{site.pk}/delete/"
    assert "students:site-delete" == resolve(f"/sites/{site.pk}/delete/").view_name


def test_site_add(site: models.Site):
    assert reverse("students:site-add") == f"/sites/add/"
    assert "students:site-add" == resolve(f"/sites/add/").view_name


def test_classroom_detail(classroom: models.Classroom):
    assert reverse("students:classroom-detail", kwargs={"pk": classroom.pk}) == f"/classrooms/{classroom.pk}/"
    assert resolve(f"/classrooms/{classroom.pk}/").view_name == "students:classroom-detail"


def test_classroom_list():
    assert reverse("students:classroom-list") == "/classrooms/"
    assert resolve("/classrooms/").view_name == "students:classroom-list"


def test_classroom_update(classroom: models.Classroom):
    assert reverse("students:classroom-update", kwargs={'pk': classroom.pk}) == f"/classrooms/{classroom.pk}/update/"
    assert "students:classroom-update" == resolve(f"/classrooms/{classroom.pk}/update/").view_name


def test_classroom_delete(classroom: models.Classroom):
    assert reverse("students:classroom-delete", kwargs={'pk': classroom.pk}) == f"/classrooms/{classroom.pk}/delete/"
    assert "students:classroom-delete" == resolve(f"/classrooms/{classroom.pk}/delete/").view_name


def test_classroom_add(classroom: models.Classroom):
    assert reverse("students:classroom-add") == f"/classrooms/add/"
    assert "students:classroom-add" == resolve(f"/classrooms/add/").view_name


def test_student_detail(student: models.Student):
    assert reverse("students:student-detail", kwargs={"pk": student.pk}) == f"/students/{student.pk}/"
    assert resolve(f"/students/{student.pk}/").view_name == "students:student-detail"


def test_student_list():
    assert reverse("students:student-list") == "/students/"
    assert resolve("/students/").view_name == "students:student-list"


def test_student_update(student: models.Student):
    assert reverse("students:student-update", kwargs={'pk': student.pk}) == f"/students/{student.pk}/update/"
    assert "students:student-update" == resolve(f"/students/{student.pk}/update/").view_name


def test_student_delete(student: models.Student):
    assert reverse("students:student-delete", kwargs={'pk': student.pk}) == f"/students/{student.pk}/delete/"
    assert "students:student-delete" == resolve(f"/students/{student.pk}/delete/").view_name


def test_student_add(student: models.Student):
    assert reverse("students:student-add") == f"/students/add/"
    assert "students:student-add" == resolve(f"/students/add/").view_name
