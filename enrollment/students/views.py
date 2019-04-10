import logging
from os import getenv
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from enrollment.students import models

logger = logging.getLogger('enrollment.students.views')
account_sid = getenv('TWILIO_SID')
auth_token = getenv('TWILIO_TOKEN')
client = Client(account_sid, auth_token)


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = models.Student


class StudentListView(LoginRequiredMixin, ListView):
    model = models.Student


class StudentCreate(LoginRequiredMixin, CreateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date']


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date']


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = models.Student
    success_url = reverse_lazy('students:student-list')


class AddressDetailView(LoginRequiredMixin, DetailView):
    model = models.Address


class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address


class AddressCreate(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = ['address_1', 'address_2', 'city', 'state', 'zip_code']


class AddressUpdate(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ['address_1', 'address_2', 'city', 'state', 'zip_code']


class AddressDelete(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy('students:address-list')


class ParentDetailView(LoginRequiredMixin, DetailView):
    model = models.Parent


class ParentListView(LoginRequiredMixin, ListView):
    model = models.Parent


class ParentCreate(LoginRequiredMixin, CreateView):
    model = models.Parent
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'students', 'address']


class ParentUpdate(LoginRequiredMixin, UpdateView):
    model = models.Parent
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'students', 'address']


class ParentDelete(LoginRequiredMixin, DeleteView):
    model = models.Parent
    success_url = reverse_lazy('students:parent-list')


@csrf_exempt
def sms_response(request):
    if request.method != 'POST':
        return HttpResponse(f'{request.method} request not supported', status=405)
    from_number = request.POST.get('From')
    body = request.POST.get('Body')
    logger.debug(from_number)
    logger.debug(body)

    # authenticate
    code = getenv('SMS_PIN')
    if code is None:
        logger.error('No SMS PIN is set')
        return HttpResponse('PIN code missing on server', status=500)
    if not body.strip().startswith(code):
        logger.warning('Incorect PIN')
        logger.warning(body)
        resp = MessagingResponse()
        resp.message("Incorrect PIN")
        return HttpResponse(str(resp))
    else:
        resp = MessagingResponse()
        message = body[len(code):]
        resp.message(f"Your message has been sent: {message}")

    parent_phone_numbers = models.Parent.objects.\
        values_list('phone_number', flat=True).\
        distinct('phone_number')
    logger.debug(parent_phone_numbers)

    if not from_number:
        logger.debug('No phone number; must be testing')
        return HttpResponse(str(resp))

    for to_number in parent_phone_numbers:
        message = client.messages.create(
            body=message,
            from_='+17472394729',
            to=to_number,
        )
        logger.debug(f'Twilio message to {to_number} SID {message.sid}')

    return HttpResponse(str(resp))

