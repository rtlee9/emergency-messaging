import logging
from os import getenv
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect

from enrollment.students import models

logger = logging.getLogger(__name__)


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

    def form_valid(self, form):
        """ If coming from parent creation then associate this address with
        that parent and return parent view.
        """
        parent_id = self.request.GET.get('parent_id')
        if parent_id:
            try:
                parent = models.Parent.objects.get(pk=parent_id)
            except models.Parent.DoesNotExist:
                logger.warning(f'Parent ID {parent_id} does not exist ({self})')
                return super().form_valid(form)
            logger.debug(f'Parent for {self} is {parent}')
            logger.debug(form.instance)
            response = super().form_valid(form)
            parent.address = form.instance
            parent.save(update_fields=['address'])
            redirect_url_base = reverse_lazy('students:parent-detail', kwargs={'pk': parent_id})
            return HttpResponseRedirect(f'{redirect_url_base}?address_id={form.instance.pk}')
        return super().form_valid(form)


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

    def get_initial(self):
        return {
            'students': self.request.GET.getlist('student_id'),
            'address': self.request.GET.getlist('address_id'),
        }

    def form_valid(self, form):
        """ If address is empty then redirect to address creation.
        """
        response = super().form_valid(form)
        if not form.data['address']:
            redirect_url_base = reverse_lazy('students:address-add')
            return HttpResponseRedirect(f'{redirect_url_base}?parent_id={form.instance.pk}')
        else:
            return response


class ParentUpdate(LoginRequiredMixin, UpdateView):
    model = models.Parent
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'students', 'address']

    def get_initial(self):
        return {
            'students': self.request.GET.getlist('student_id'),
        }


class ParentDelete(LoginRequiredMixin, DeleteView):
    model = models.Parent
    success_url = reverse_lazy('students:parent-list')
