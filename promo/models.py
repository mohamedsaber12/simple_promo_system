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

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

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

    def use_points(self, points_to_use=0):
        # check if points to use is less than or equal promo amount
        if (points_to_use > self.promo_amount):
            raise ValidationError(f"Your promo points is less than {points_to_use}")
        remaining_points = self.promo_amount - points_to_use
        self.promo_amount = remaining_points
        super(Promo, self).save()

