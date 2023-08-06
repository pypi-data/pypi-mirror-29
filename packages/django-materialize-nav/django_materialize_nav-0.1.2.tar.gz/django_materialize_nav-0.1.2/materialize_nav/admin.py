from django.contrib import admin
from django.conf import settings


if settings.AUTH_USER_MODEL == 'materialize_nav.User':
    from .models import User

    admin.site.register(User)
