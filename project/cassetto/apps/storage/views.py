from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseNotFound
from rest_framework import viewsets
from rest_framework import permissions
from sendfile import sendfile

from ...permissions import IsStorageUser, IsStorageResourceUser
from .models import Storage, Resource
from .serializers import StorageSerializer, StorageDetailSerializer, ResourceSerializer


def download_view(request, username, storage, path):
    """
    Return HttpResponse object for serving file

    :param request:
    :param username:
    :param storage:
    :param resource:
    :return:
    """
    if not path.startswith('/'):
        path = '/' + path
    try:
        resource = Resource.objects.get(
            storage__code=storage,
            storage__owner__username=username,
            path=path
        )
    except Resource.DoesNotExist:
        return HttpResponseNotFound()

    if not IsStorageResourceUser().has_object_permission(request, download_view, resource):
        return HttpResponseForbidden()

    return sendfile(request, resource.file.path, attachment=True)


##### API Views #####
class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = (IsStorageUser, )

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        """
        Display only storage owned by or shared with current user.
        """
        user = self.request.user
        query = Q(owner__pk=user.pk) | Q(sharing__user__pk=user.pk)
        return Storage.objects.filter(query)

    def get_serializer_class(self):
        """
        Display resource list for detail view
        """
        if getattr(self, 'object', False):
            return StorageDetailSerializer
        return super(StorageViewSet, self).get_serializer_class()


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (IsStorageResourceUser, )

    def get_queryset(self):
        """
        Display only resources contained in a storage owned by or shared with current user.
        """
        user = self.request.user
        query = Q(uploader__pk=user.pk) | Q(storage__owner__pk=user.pk) | Q(storage__sharing__user__pk=user.pk)
        return Resource.objects.filter(query)

    def pre_save(self, obj):
        obj.uploader = self.request.user
##### END API Views #####

