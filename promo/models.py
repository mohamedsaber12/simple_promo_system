from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField
from django.core.exceptions import ValidationError

# Users Models


class User(AbstractUser):
    class Types(models.TextChoices):
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
        NORMAL = "NORMAL", "Normal"

    base_type = Types.ADMINISTRATOR

    type = models.CharField(_("Type"),
                            max_length=50,
                            choices=Types.choices,
                            default=base_type)

    address = models.CharField(_("Name of User"), blank=True, max_length=255)


class AdministratorUser(User):
    class Meta:
        verbose_name = "Administrator User"

    base_type = User.Types.ADMINISTRATOR

    def save(self, *args, **kwargs):
        self.type = User.Types.ADMINISTRATOR
        super(AdministratorUser, self).save(*args, **kwargs)


class NormalUser(User):
    class Meta:
        verbose_name = "Normal User"

    base_type = User.Types.NORMAL
    mobile_number = PhoneField(blank=True, help_text='user mobile number')

    def save(self, *args, **kwargs):
        self.type = User.Types.NORMAL
        super(NormalUser, self).save(*args, **kwargs)


# End of users model

# Promo Model


class Promo(models.Model):
    BOOL_CHOICES = [(True, "Yes"), (False, "No")]

    user = models.ForeignKey(
        NormalUser,
        on_delete=models.CASCADE,
        related_name="promos",
    )
    promo_type = models.CharField(max_length=200)
    promo_code = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    promo_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True, choices=BOOL_CHOICES)

    @property
    def total_used_points(self):
        return sum(p.number_of_points for p in self.promos_use.all())

    @property
    def remaining_points(self):
        return self.promo_amount - self.total_used_points


class PromoUse(models.Model):
    promo = models.ForeignKey(Promo,
                              on_delete=models.CASCADE,
                              related_name="promos_use")
    number_of_points = models.DecimalField(max_digits=10, decimal_places=1)
    creation_time = models.DateTimeField(auto_now_add=True)
