from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Message(models.Model):
    sid = models.CharField(max_length=34, primary_key=True)
    from_phone_number = PhoneNumberField()
    to_phone_number = PhoneNumberField()
    body = models.CharField(max_length=160)


class MessageStatus(models.Model):
    status = models.CharField(max_length=12, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    sid = models.CharField(max_length=34)
