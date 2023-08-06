"""
Add thumbnail and background_image to the User Model.

Settings to override:
    PROFILE_THUMBNAIL_DIRECTORY  = "accounts/thumbnail"  # Media folder
    PROFILE_THUMBNAIL_DEFAULT    = "accounts/default_user.png"  # Static file
    PROFILE_BACKGROUND_DIRECTORY = "accounts/background"  # Media folder
    PROFILE_BACKGROUND_DEFAULT   = "accounts/default_background.png"  # Static file
"""
import os
from django.db import models

# Import the user model. This needs to be here after the settings are imported.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static


# ===== Additional settings =====
settings.PROFILE_THUMBNAIL_DIRECTORY = getattr(settings, "PROFILE_THUMBNAIL_DIRECTORY", "materialize_nav/accounts/thumbnail")
settings.PROFILE_THUMBNAIL_DEFAULT = getattr(settings, "PROFILE_THUMBNAIL_DEFAULT", "materialize_nav/accounts/default_user.png")
settings.PROFILE_BACKGROUND_DIRECTORY = getattr(settings, "PROFILE_BACKGROUND_DIRECTORY", "materialize_nav/accounts/background")
settings.PROFILE_BACKGROUND_DEFAULT = getattr(settings, "PROFILE_BACKGROUND_DEFAULT", "materialize_nav/accounts/default_background.png")


def get_default_thumbnail():
    """Return the default thumbnail image from the settings."""
    return static(settings.PROFILE_THUMBNAIL_DEFAULT)


def get_default_background():
    """Return the default background image from the settings."""
    return static(settings.PROFILE_BACKGROUND_DEFAULT)


def get_thumbnail_save(obj, file=None):
    """Return the thumbnail directory from the settings.

    Args:
        obj (object/User): Object to get the username from.
        file (str)[None]: Filename to use if obj.instance.username does not exist.

    Returns:
        filename (str): Thumbnail save filename
    """
    try:
        fname = (str(obj.instance.username) + "_thumbnail.png").replace(" ", "_")
    except:
        fname = (str(obj) + "_thumbnail.png").replace(" ", "_")

    return os.path.join(settings.PROFILE_THUMBNAIL_DIRECTORY, fname)


def get_background_save(obj, file=None):
    """Return the background image directory from the settings.

    Args:
        obj (object/User): Object to get the username from.
        file (str)[None]: Filename to use if obj.instance.username does not exist.

    Returns:
        filename (str): Background image save filename
    """
    try:
        fname = (str(obj.instance.username) + "_background.png").replace(" ", "_")
    except:
        fname = (str(obj) + "_background.png").replace(" ", "_")

    return os.path.join(settings.PROFILE_BACKGROUND_DIRECTORY, fname)


class OverwriteStorage(FileSystemStorage):
    """Storage that overwrites existing files when saving a file."""
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, *args, **kwargs):
        return name


if settings.AUTH_USER_MODEL == 'materialize_nav.User':
    class User(AbstractUser):
        """New user that has a thumbnail and background image."""

        thumbnail = models.ImageField(upload_to=get_thumbnail_save, storage=OverwriteStorage(), blank=True, null=True)
        background_image = models.ImageField(upload_to=get_background_save, storage=OverwriteStorage(), blank=True, null=True)

        @classmethod
        def get_default_thumbnail(cls):
            return static(settings.PROFILE_THUMBNAIL_DEFAULT)

        @classmethod
        def get_default_background_image(cls):
            return static(settings.PROFILE_BACKGROUND_DEFAULT)

        class Meta:
            # Do not create the database table unless this is the User model (still causes migration issues at times)
            managed = settings.AUTH_USER_MODEL == 'materialize_nav.User'
