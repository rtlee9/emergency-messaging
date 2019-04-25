from factory import DjangoModelFactory, Faker, post_generation, Iterator
from enrollment.students import models
from faker.providers import phone_number
import phonenumbers

# the PhoneNumberField uses the phonenumbers package which uses
# actual data to check if a phone number is valid (e.g., some
# are codes aren't actually used); need to mock it instead
phonenumbers.is_valid_number = phonenumbers.is_possible_number


# override default faker formats (less format variability)
provider = phone_number.Provider
provider.formats = ('+1##########',)
Faker('phone_number').add_provider(provider)


def iter_random(model):
    while True:
        yield model.objects.order_by('?').first()


class SiteFactory(DjangoModelFactory):
    name = Faker('sentence', nb_words=4)

    class Meta:
        model = models.Site


class ClassroomFactory(DjangoModelFactory):
    name = Faker('sentence', nb_words=4)
    site = Iterator(iter_random(models.Site))

    class Meta:
        model = models.Classroom


class StudentFactory(DjangoModelFactory):

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    birth_date = Faker('date')
    classroom = Iterator(iter_random(models.Classroom))

    class Meta:
        model = models.Student


class ParentFactory(DjangoModelFactory):

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone_number = Faker('phone_number')
    email = Faker('email')

    class Meta:
        model = models.Parent

    @post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for student in extracted:
                self.students.add(student)
