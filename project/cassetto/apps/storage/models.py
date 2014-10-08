from django.conf import settings
from django.db import models


class Storage(models.Model):

    name = models.CharField(max_length=settings['CASSETTO'].get('STORAGE_NAME_MAX_LENGTH'))
    slug = models.SlugField(max_length=255)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resource(models.Model):

    name = models.CharField(max_length=settings['CASSETTO'].get('FILENAME_MAX_LENGTH'))
    description = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    path = models.TextField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    cassetto = models.ForeignKey(Storage, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
