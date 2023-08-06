from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin

from .models import User

if settings.AUTH_USER_MODEL == 'materialize_nav.User':
    from .models import User

    ADDITIONAL_USER_FIELDS = (
        (None, {'fields': ("thumbnail", "background_image")}),
    )

    class MaterializeUserAdmin(UserAdmin):
        add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
        fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

    admin.site.register(User, MaterializeUserAdmin)
