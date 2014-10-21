from django.conf import settings
from django.db import models


class Storage(models.Model):

    code = models.SlugField(max_length=settings.CASSETTO.get('STORAGE_NAME_MAX_LENGTH'))
    description = models.TextField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='storages')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (
            ('owner', 'code'),
        )


class Resource(models.Model):

    path = models.TextField()
    name = models.CharField(max_length=settings.CASSETTO.get('FILENAME_MAX_LENGTH'))
    description = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resources')
    storage = models.ForeignKey(Storage, blank=True, null=True, related_name='resources')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (
            ('storage', 'path')
        )
