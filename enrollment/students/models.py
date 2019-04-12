from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_localflavor_us.models import USStateField
from django.urls import reverse


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True


class Address(models.Model):
    address_1 = models.CharField(("address"), max_length=128)
    address_2 = models.CharField(("address cont'd"), max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = USStateField()
    zip_code = models.CharField(max_length=5)

    class Meta:
        ordering = ['address_1']

    def __str__(self):
        return f"""
        {self.address_1}
        {self.address_2}
        {self.city} {self.state}, {self.zip_code}
        """

    def get_absolute_url(self):
        return reverse('students:address-detail', kwargs={'pk': self.pk})


class Student(Person):
    birth_date = models.DateField()

    class Meta:
        ordering = ['first_name', 'last_name', 'birth_date']

    def get_absolute_url(self):
        return reverse('students:student-detail', kwargs={'pk': self.pk})


class Parent(Person):
    students = models.ManyToManyField(Student)
    email = models.EmailField()
    phone_number = PhoneNumberField(unique=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('students:parent-detail', kwargs={'pk': self.pk})


class ClassRoom(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Student, through='Membership')


class Membership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date_joined = models.DateField()
    tution = models.PositiveIntegerField(null=True, blank=True)
