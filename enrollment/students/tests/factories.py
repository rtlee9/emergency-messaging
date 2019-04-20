from factory import DjangoModelFactory, Faker
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


class ParentFactory(DjangoModelFactory):

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone_number = Faker('phone_number')
    email = Faker('email')

    class Meta:
        model = models.Parent
        django_get_or_create = ['phone_number']


class SiteFactory(DjangoModelFactory):
    name = Faker('sentence', nb_words=4)

    class Meta:
        model = models.Site
