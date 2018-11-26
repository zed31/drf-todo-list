from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.core.cache import cache
from django.core import serializers
from . import constants
from .models import TodoListModel, UserModel
from .permissions import IsAdmin, IsNotBanned, IsOwnerOrAdminOrReadOnly, IsOwnerOrAdmin, IsSameUserOrAdmin
from .serializers import TodoListSerializer, UserSerializer
from . import urls_name
from . import request_utils

# Create your views here.
class CreateAdminTodo(generics.CreateAPIView):
    serializer_class = TodoListSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin, IsNotBanned,)

    """
        Only used by the administrator to create
        task to any users
    """
    def post(self, request, format=None):
        """
            Post request to create todo when you are an administrator

            :param self: The class itself
            :param request: The post request
            :param format: The format of the request
        """
        try:
            owner_email = request.data['owner']
            task_owner = UserModel.objects.get(email=owner_email)
            task = TodoListModel(title=request.data['title'], description=request.data['description'], owner=task_owner)
            task.save()
            serializer = TodoListSerializer(task)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': 'Fields required: title, description and owner'})
        

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
    permission_classes = (IsAdmin, IsNotBanned,)

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    """
        Detail the specific user from the database
        also allows the update and the destroy of this
        specific user
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSameUserOrAdmin, IsNotBanned,)

class MeTodo(generics.ListAPIView):
    """
        Me todo, used to retrieve ONLY the todo of an user
    """
    queryset = TodoListModel
    serializer_class = TodoListSerializer
    permission_classes = (permissions.IsAuthenticated, IsNotBanned,)

    def get(self, request, format=None):
        """
            Get specific task from a specific email stored inside the cache
            :param self: the self-class
            :param request: the Request being processed
            :param format: the format of the request
            :return: Response with status code and JSON serialized data
        """
        objects = TodoListModel.objects.filter(owner__email=request.user.email)
        serializer = TodoListSerializer(objects, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
        

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
