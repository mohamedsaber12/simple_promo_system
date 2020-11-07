from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField


class User(AbstractUser):
    class Types(models.TextChoices):
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
        NORMAL = "NORMAL", "Normal"

    base_type = Types.ADMINISTRATOR

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    address = models.CharField(_("Name of User"), blank=True, max_length=255)

class Administrator(User):
    base_type = User.Types.ADMINISTRATOR

class Normal(User):
    base_type = User.Types.NORMAL
    mobile_number = PhoneField(blank=True, help_text='user mobile number')
