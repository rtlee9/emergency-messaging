from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from enrollment.students import models


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = models.Student


class StudentListView(LoginRequiredMixin, ListView):
    model = models.Student


class StudentCreate(CreateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date']


class StudentUpdate(UpdateView):
    model = models.Student
    fields = ['first_name', 'last_name', 'birth_date']


class StudentDelete(DeleteView):
    model = models.Student
    success_url = reverse_lazy('students:student-list')


class ParentDetailView(LoginRequiredMixin, DetailView):
    model = models.Parent


class ParentListView(LoginRequiredMixin, ListView):
    model = models.Parent


class ParentCreate(CreateView):
    model = models.Parent
    fields = ['first_name', 'last_name', 'email', 'phone_number']


class ParentUpdate(UpdateView):
    model = models.Parent
    fields = ['first_name', 'last_name', 'email', 'phone_number']


class ParentDelete(DeleteView):
    model = models.Parent
    success_url = reverse_lazy('students:parent-list')
