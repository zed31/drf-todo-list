from rest_framework import permissions

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
        Custom permission decorator to enable only
        the owner of a task, otherwise it's a read only
        method
    """

    def has_object_permission(self, request, view, obj):
        """
            Read permissions and check if the requested
            object can be returned

            :param self: the IsOwnerOrReadOnly class
            :param request: the request made by the user
            :param view: the impacted view of the request
            :param obj: the requested object
        """

        return True if request.method in permissions.SAFE_METHODS or obj.owner == request.user.owner or request.user.is_admin else False
