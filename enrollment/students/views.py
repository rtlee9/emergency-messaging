import logging
from os import getenv
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

from enrollment.students import models

logger = logging.getLogger('enrollment.students.views')


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
    # Start our TwiML response
    body = request.POST.get('Body')
    logger.debug(body)
    resp = MessagingResponse()

    # authenticate
    code = getenv('SMS_PIN')
    if code is None:
        logger.error('No SMS PIN is set')
        return HttpResponse('PIN code missing on server', status=500)
    if not body.strip().startswith(code):
        resp.message("Incorrect PIN")
    else:
        message = body[len(code):]
        resp.message(f"Your message has been sent: {message}")

    return HttpResponse(str(resp))
