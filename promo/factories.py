import factory
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker
from faker import Faker as Fake
from .models import NormalUser, AdministratorUser, Promo, PromoUse

User = get_user_model()

fake = Fake()


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    first_name = Faker("name")
    last_name = Faker("name")

    class Meta:
        model = User


class NormalUserFactory(UserFactory):
    type = "NORMAL"

    class Meta:
        model = NormalUser


class AdministratorUserFactory(UserFactory):
    type = "ADMINISTRATOR"

    class Meta:
        model = AdministratorUser


class PromoFactory(DjangoModelFactory):
    user = factory.SubFactory("promo.factories.NormalUserFactory")
    promo_type = Faker("name")
    promo_code = Faker("name")
    description = Faker("sentence")
    start_date = Faker("date")
    end_date = Faker("date")
    promo_amount = fake.pyint()
    is_active = True

    class Meta:
        model = Promo


class PromoUseFactory(DjangoModelFactory):
    promo = factory.SubFactory("promo.factories.PromoFactory")
    number_of_points = fake.pyint()

    class Meta:
        model = PromoUse
