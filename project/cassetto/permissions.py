from rest_framework import permissions
from cassetto.apps.sharing.models import Sharing


class IsOwner(permissions.BasePermission):

    @property
    def owner_field_name(self):
        raise NotImplementedError

    def has_object_permission(self, request, view, obj):
        return request.user == getattr(obj, self.owner_field_name)


class IsResourceOwner(IsOwner):
    owner_field_name = 'uploader'


class IsStorageOwner(IsOwner):
    owner_field_name = 'owner'


class IsStorageUser(IsStorageOwner):

    def has_object_permission(self, request, view, obj):

        if super(IsStorageUser, self).has_object_permission(request, view, obj):
            return True

        try:
            sharing = obj.sharing_set.get(user=request.user)

            if sharing.policy == Sharing.POLICY_READ_ONLY:
                # check if user wants to edit something
                return request.method in permissions.SAFE_METHODS

            return True

        except Sharing.DoesNotExist:
            return False

class IsStorageResourceUser(IsStorageUser):

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated() and request.user == obj.uploader:
            return True

        return super(IsStorageResourceUser, self).has_object_permission(request, view, obj.storage)
#
# class IsSharedResource(IsSharedStorage):
#
#     def has_object_permission(self, request, view, obj):
#         return super(IsSharedResource, self).has_object_permission(request, view, obj.storage)
#
#
# class IsOwnerOrShared(permissions.IsAuthenticated):
#
#
#
#
#     def has_object_permission(self, request, view, obj):
#         # Write permissions are only allowed to the owner.
#         if obj.owner == request.user:
#             return True
#
#         if hasattr(obj, 'storage'):
#             # if object is a resource we have to check its storage
#             return self.has_object_permission(request, view, obj.storage)
#
#         try:
#             sharing = obj.sharing_set.get(user=request.user)
#
#             if sharing.policy == Sharing.POLICY_READ_ONLY:
#                 # check if user wants to edit something
#                 return request.method in permissions.SAFE_METHODS
#
#             return True
#
#         except Sharing.DoesNotExist:
#             return False
