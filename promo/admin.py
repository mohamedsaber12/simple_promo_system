from django.contrib import admin

# Register your models here.

from promo.models import Promo, NormalUser, AdministratorUser, User

class PromoAdmin(admin.ModelAdmin):
    pass

class NormalUserAdmin(admin.ModelAdmin):
    pass

class AdministratorUserAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Promo, PromoAdmin)
admin.site.register(NormalUser, NormalUserAdmin)
admin.site.register(AdministratorUser, AdministratorUserAdmin)
admin.site.register(User, UserAdmin)

