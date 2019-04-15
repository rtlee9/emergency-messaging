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
    fields = ['first_name', 'last_name', 'birth_date', 'classroom']


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date', 'classroom']


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
        """ If coming from classroom creation then associate this address with
        that classroom and return classroom view.
        """
        classroom_id = self.request.GET.get('classroom_id')
        if classroom_id:
            try:
                classroom = models.Site.objects.get(pk=classroom_id)
            except models.Site.DoesNotExist:
                logger.warning(f'Site ID {classroom_id} does not exist ({self})')
                return super().form_valid(form)
            logger.debug(f'Site for {self} is {classroom}')
            logger.debug(form.instance)
            response = super().form_valid(form)
            classroom.address = form.instance
            classroom.save(update_fields=['address'])
            redirect_url_base = reverse_lazy('students:classroom-detail', kwargs={'pk': classroom_id})
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


class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = models.Classroom


class ClassroomListView(LoginRequiredMixin, ListView):
    model = models.Classroom


class ClassroomCreate(LoginRequiredMixin, CreateView):
    model = models.Classroom
    fields = ['name', 'site']


class ClassroomUpdate(LoginRequiredMixin, UpdateView):
    model = models.Classroom
    fields = ['name', 'site']


class ClassroomDelete(LoginRequiredMixin, DeleteView):
    model = models.Classroom
    success_url = reverse_lazy('students:classroom-list')


class SiteDetailView(LoginRequiredMixin, DetailView):
    model = models.Site


class SiteListView(LoginRequiredMixin, ListView):
    model = models.Site


class SiteCreate(LoginRequiredMixin, CreateView):
    model = models.Site
    fields = ['name']


class SiteUpdate(LoginRequiredMixin, UpdateView):
    model = models.Site
    fields = ['name']


class SiteDelete(LoginRequiredMixin, DeleteView):
    model = models.Site
    success_url = reverse_lazy('students:site-list')
