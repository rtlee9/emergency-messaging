from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from enrollment.students.models import Parent


class Message(models.Model):
    sid = models.CharField(max_length=34, primary_key=True)
    from_phone_number = PhoneNumberField()
    to_phone_number = PhoneNumberField()
    body = models.CharField(max_length=160)
    from_parent = models.ForeignKey(
        Parent, null=True, on_delete=models.SET_NULL, related_name='from_parent')
    to_parent = models.ForeignKey(
        Parent, null=True, on_delete=models.SET_NULL, related_name='to_parent')


class MessageStatus(models.Model):
    status = models.CharField(max_length=12, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    sid = models.CharField(max_length=34)
