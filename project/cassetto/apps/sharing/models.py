from django.conf import settings
from django.db import models


class Sharing(models.Model):

    POLICY_READ_ONLY = 0
    POLICY_EDITABLE = 1

    policy = models.PositiveSmallIntegerField(choices=(
        (POLICY_READ_ONLY, 'read-only'),
        (POLICY_EDITABLE, 'editable'),
    ))

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    storage = models.ForeignKey('storage.Storage')

    shared_at = models.DateTimeField(auto_now_add=True, editable=False)


class Publication(models.Model):

    path = models.TextField()

    resource = models.ForeignKey('storage.Resource')

    published_at = models.DateTimeField(auto_now_add=True, editable=False)