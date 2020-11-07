from django.contrib import admin

# Register your models here.

from promo.models import Promo, NormalUser, AdministratorUser

class PromoAdmin(admin.ModelAdmin):
    pass

class NormalUserAdmin(admin.ModelAdmin):
    pass

class AdministratorUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Promo, PromoAdmin)
admin.site.register(NormalUser, NormalUserAdmin)
admin.site.register(AdministratorUser, AdministratorUserAdmin)

