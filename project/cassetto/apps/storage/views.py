from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions

from ...permissions import IsOwnerOrShared
from .models import Storage, Resource
from .serializers import StorageSerializer, StorageDetailSerializer, ResourceSerializer


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrShared, )

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
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrShared, )

    def get_queryset(self):
        """
        Display only resources contained in a storage owned by or shared with current user.
        """
        user = self.request.user
        query = Q(owner__pk=user.pk) | Q(storage__owner__pk=user.pk) | Q(storage__sharing__user__pk=user.pk)
        return Resource.objects.filter(query)

    def pre_save(self, obj):
        obj.owner = self.request.user

