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

        return True if request.method in permissions.SAFE_METHODS or obj.owner == request.user or request.user.is_superuser else False

class IsAdmin(permissions.BasePermission):
    """
        Check if the user is an administrator
    """
    def has_object_permission(self, request, view, obj):
        """
            Check if the user is a superuser. Basically a superuser
            is an administrator inside our database

            :param self: The IsAdmin class this
            :param request: The request made by the user
            :param view: The impacted view of the request
            :param obj: The requested object

            :return: True if the user is a superuser, False otherwise
        """
        return request.user.is_superuser

class IsNotBanned(permissions.BasePermission):
    """
        Check if the user is ban and can access or not
        to the page
    """
    def has_object_permission(self, request, view, obj):
        """
            Check if the user is not ban

            :param self: The IsNotBanned class
            :param request: The request made by the user
            :param view: The view impacted by the request
            :param obj: The requested object

            :return: True if the user is not ban, False otherwise
        """
        return not request.user.is_ban
