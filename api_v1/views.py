from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import TodoListModel, UserModel
from .permissions import IsAdmin, IsNotBanned, IsOwnerOrAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import TodoListSerializer, UserSerializer
from . import urls_name
from . import constants
from . import request_utils

# Create your views here.
class ListTodo(generics.ListCreateAPIView):
    """
        List all the todo present inside the database
        also allows POST request to create some
    """
    queryset = TodoListModel.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (permissions.IsAuthenticated, IsNotBanned,)

    def perform_create(self, serializer):
        """
            Override the perform_create from the generic
            serializers.

            :param self: Class
            :param serializer: serializer used to perform actions
        """
        serializer.save(owner=self.request.user)

class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    """
        Detail the specific todo present inside the
        database
    """
    queryset = TodoListModel.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin, IsNotBanned,)

class ListUser(generics.ListCreateAPIView):
    """
        List all users from the database
        also allows POST request to create some
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdmin, IsNotBanned,)

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    """
        Detail the specific user from the database
        also allows the update and the destroy of this
        specific user
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsNotBanned,)

def generate_method_information(route_name, request, format, methods):
    """
        Generate a method information with the URI and the different
        available method

        :param route_name: The name of the route
        :param request: The request actually made
        :param format: The format of the request
        :param methods: The different methods available
    """
    return {
        constants.URI_KEY: reverse(route_name, request=request, format=format),
        constants.METHOD_KEY: methods,
    }

@api_view(['GET'])
def api_root(request, format=None):
    """
        This response is returned each time a root is not found just to show
        to the user the different root he can go to

        :param request: The request being made
        :param format: The current format of the request
    """
    response = {constants.TODO_LIST_URI_INFO: generate_method_information(urls_name.TODO_LIST_NAME, request=request, format=format, methods=[constants.GET_METHOD])}
    if request_utils.is_user_authenticated(request):
        response[constants.TODO_LIST_URI_INFO][constants.METHOD_KEY] = [constants.GET_METHOD, constants.POST_METHOD]
        response[constants.LOGOUT_URI_INFO] = generate_method_information(urls_name.LOGOUT_NAME, request=request, format=format, methods=[constants.GET_METHOD])

        if request_utils.is_user_admin(request):
            response[constants.USER_LIST_URI_INFO] = generate_method_information(urls_name.USER_LIST_NAME, request=request, format=format, methods=[constants.GET_METHOD, constants.POST_METHOD])
    else:
        response[constants.REGISTRATION_URI_INFO] = generate_method_information(urls_name.REGISTER_NAME, request=request, format=format, methods=[constants.POST_METHOD])
        response[constants.LOGIN_URI_INFO] = generate_method_information(urls_name.LOGIN_NAME, request=request, format=format, methods=[constants.POST_METHOD])
    return Response(response)
