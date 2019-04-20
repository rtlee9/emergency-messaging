from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class Message(models.Model):
    sid = models.CharField(max_length=34, primary_key=True)
    from_phone_number = PhoneNumberField()
    to_phone_number = PhoneNumberField()
    body = models.CharField(max_length=160)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    msg_type = models.CharField(max_length=32)

    # constants
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'
    CONFIRMATION = 'confirmation'
    SITE_PROMPT = 'site_prompt'

    def get_absolute_url(self):
        return reverse('messaging:message-detail', kwargs={'sid': self.sid})

    def __str__(self):
        return f'''
        From: {self.from_phone_number}
        To: {self.to_phone_number}
        Body: {self.body}
        '''


class MessageStatus(models.Model):
    status = models.CharField(max_length=12, null=True)  # TODO: validate status
    datetime = models.DateTimeField(auto_now_add=True)
    sid = models.CharField(max_length=34)

    # constants
    AUTH_FAIL = 'auth_fail'
    AUTH_PASS = 'auth_pass'
    AUTH_SKIP = 'auth_skip'
    TWILIO_QUEUED = 'queued'
    TWILIO_FAILED = 'failed'
    TWILIO_SENT = 'sent'
    TWILIO_DELIVERED = 'delivered'
    TWILIO_UNDELIVERED = 'undelivered'
    STATUS_CHOICES = (
        AUTH_FAIL,
        AUTH_PASS,
        AUTH_SKIP,
        TWILIO_QUEUED,
        TWILIO_FAILED,
        TWILIO_SENT,
        TWILIO_DELIVERED,
        TWILIO_UNDELIVERED,
    )

    class Meta:
        get_latest_by = 'datetime'

    def __str__(self):
        return f'{self.sid} was {self.status} on {self.datetime}'
