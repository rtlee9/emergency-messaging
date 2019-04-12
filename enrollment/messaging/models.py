from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from enrollment.students.models import Parent


class Message(models.Model):
    from_phone_number = PhoneNumberField()
    to_phone_number = PhoneNumberField()
    body = models.CharField(max_length=160)
    sid = models.CharField(max_length=34, null=True)
    # status
    from_parent = models.ForeignKey(
        Parent, null=True, on_delete=models.SET_NULL, related_name='from_parent')
    to_parent = models.ForeignKey(
        Parent, null=True, on_delete=models.SET_NULL, related_name='to_parent')
