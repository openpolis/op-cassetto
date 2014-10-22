from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import hashlib
from mimetypes import MimeTypes
mime = MimeTypes()

def generate_checksum(file):
    sha = hashlib.sha1()
    file.seek(0)

    while True:
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    checksum = sha.hexdigest()

    # to make sure later operations can read the whole file
    file.seek(0)

    return checksum


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

    path = models.TextField(blank=True)
    name = models.CharField(max_length=settings.CASSETTO.get('FILENAME_MAX_LENGTH'), blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='storage/', blank=True, null=True)
    mime_type = models.CharField(max_length=255, editable=False)
    checksum = models.CharField(max_length=70, editable=False)
    encoding = models.CharField(max_length=10, blank=True, editable=False)
    file_size = models.PositiveIntegerField(editable=False)

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resources')
    storage = models.ForeignKey(Storage, blank=True, null=True, related_name='resources')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        # resolve name
        if not self.name:
            self.name = self.file.name

        # fix path
        if not self.path:
            self.path = self.file.name
        if not self.path.startswith('/'):
            self.path = '/' + self.path

        # detect meta about file
        self.mime_type, self.encoding = mime.guess_type(self.file.path)
        if self.encoding is None:
            self.encoding = ''
        self.file_size = self.file.size
        self.checksum = generate_checksum(self.file)

        return super(Resource, self).save(*args, **kwargs)

    def get_download_url(self):
        return reverse('resource-download', kwargs={
            'username': self.uploader.username,
            'storage': self.storage.code,
            'path': self.path[1:] or self.file.name,
        })

    class Meta:
        unique_together = (
            ('storage', 'path')
        )
