from factory import DjangoModelFactory, Faker, fuzzy
from enrollment.messaging import models
from faker.providers import phone_number

# override default faker formats (less format variability)
provider = phone_number.Provider
provider.formats = ('+1-###-###-####',)
Faker('phone_number').add_provider(provider)


class MessageFactory(DjangoModelFactory):

    sid = Faker('password', length=34, special_chars=False)
    body = Faker('text', max_nb_chars=160)
    from_phone_number = Faker('phone_number')
    to_phone_number = Faker('phone_number')

    class Meta:
        model = models.Message
        django_get_or_create = ["sid"]


class MessageStatusFactory(DjangoModelFactory):

    sid = Faker('password', length=34, special_chars=False)
    datetime = Faker('date_time')
    status = fuzzy.FuzzyChoice(models.MessageStatus.STATUS_CHOICES)

    class Meta:
        model = models.MessageStatus
