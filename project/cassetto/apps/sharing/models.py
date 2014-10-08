from django.conf import settings
from django.db import models


class Sharing(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    storage = models.ForeignKey('storage.Storage')

    shared_at = models.DateTimeField(auto_now_add=True)


class Publication(models.Model):

    path = models.CharField(max_length=settings.CASSETTO.get('FILENAME_MAX_LENGTH'))

    storage = models.ForeignKey('storage.Storage')

    published_at = models.DateTimeField(auto_now_add=True)