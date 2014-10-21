from rest_framework import permissions
from cassetto.apps.sharing.models import Sharing


class IsOwnerOrShared(permissions.IsAuthenticated):


    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner.
        if obj.owner == request.user:
            return True

        if hasattr(obj, 'storage'):
            # if object is a resource we have to check its storage
            return self.has_object_permission(request, view, obj.storage)

        try:
            sharing = obj.sharing_set.get(user=request.user)

            if sharing.policy == Sharing.POLICY_READ_ONLY:
                # check if user wants to edit something
                return request.method in permissions.SAFE_METHODS

            return True

        except Sharing.DoesNotExist:
            return False
