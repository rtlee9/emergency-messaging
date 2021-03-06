import logging
from os import getenv
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect

from enrollment.students import models
from enrollment.users.mixins import StaffRequiredMixin

logger = logging.getLogger(__name__)


class StudentDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = models.Student


class StudentListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = models.Student


class StudentCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date', 'classrooms']


class StudentUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date', 'classrooms']


class StudentDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = models.Student
    success_url = reverse_lazy('students:student-list')


class AddressDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = models.Address


class AddressListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = models.Address


class AddressCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = models.Address
    fields = ['address_1', 'address_2', 'city', 'state', 'zip_code']

    def get_context_data(self, **kwargs):
        parent_id = self.request.GET.get('parent_id')
        context = super().get_context_data(**kwargs)
        try:
            context['parent'] = models.Parent.objects.get(pk=parent_id)
        except models.Parent.DoesNotExist:
            logger.error(f'Parent {parent_id} does not exist')
        return context

    def form_valid(self, form):
        """ If coming from parent creation then associate this address with
        that parent and return parent view.
        """
        parent_id = self.request.GET.get('parent_id')
        if parent_id:
            try:
                parent = models.Parent.objects.get(pk=parent_id)
            except models.Parent.DoesNotExist:
                logger.warning(f'Site ID {parent_id} does not exist ({self})')
                return super().form_valid(form)
            logger.debug(f'Site for {self} is {parent}')
            logger.debug(form.instance)
            response = super().form_valid(form)
            parent.address = form.instance
            parent.save(update_fields=['address'])
            redirect_url_base = reverse_lazy('students:parent-detail', kwargs={'pk': parent_id})
            return HttpResponseRedirect(f'{redirect_url_base}?address_id={form.instance.pk}')
        return super().form_valid(form)


class AddressUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = models.Address
    fields = ['address_1', 'address_2', 'city', 'state', 'zip_code']


class AddressDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy('students:address-list')


class ParentDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = models.Parent


class ParentListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = models.Parent


class ParentCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
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


class ParentUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = models.Parent
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'students', 'address']

    def get_initial(self):
        initial = {}
        student_args = self.request.GET.getlist('student_id')
        if student_args:
            initial['students'] = student_args
        return initial


class ParentDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = models.Parent
    success_url = reverse_lazy('students:parent-list')


class ClassroomDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = models.Classroom


class ClassroomListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = models.Classroom


class ClassroomCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = models.Classroom
    fields = ['name', 'site']


class ClassroomUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = models.Classroom
    fields = ['name', 'site']


class ClassroomDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = models.Classroom
    success_url = reverse_lazy('students:classroom-list')


class SiteDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = models.Site


class SiteListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = models.Site


class SiteCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = models.Site
    fields = ['name']


class SiteUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = models.Site
    fields = ['name']


class SiteDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = models.Site
    success_url = reverse_lazy('students:site-list')
