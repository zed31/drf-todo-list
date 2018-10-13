from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .authentication import EmailBackendModel
from .models import TodoListModel, UserModel
from .permissions import IsAdmin, IsNotBanned, IsOwnerOrAdminOrReadOnly
from .serializers import TodoListSerializer, UserSerializer
from . import urls_name
from . import constants


def retrieve_email_and_password(request):
    """
        Extract the email and the password from a request

        :param request: The request
    """
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    return email, password

def is_user_authenticated(request):
    """
        Check if the session exist inside the specified
        request

        :param request: The request being analyzed
    """
    return request.session.session_key

def is_user_admin(request):
    """
        Check if the user is an administrator

        :param request: The request sent by the user
    """
    return request.user.is_superuser

# Create your views here.
class ListTodo(generics.ListCreateAPIView):
    """
        List all the todo present inside the database
        also allows POST request to create some
    """
    queryset = TodoListModel.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly, IsNotBanned,)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly, IsNotBanned,)

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

class UserAuthenticationView(APIView):
    """
        Post and generate the authentication as well as login
    """

    def post(self, request, format=None):
        """
            Post method used to authenticate the user
            check first if the user exist and if thats the case
            we just add a new session to the cache

            :param request: The request on a django request format
            :param format: The request format
        """
        email, password = retrieve_email_and_password(request)
        authentication_backend = EmailBackendModel()
        user = authentication_backend.authenticate(username=email, password=password)
        if user is None:
            return Response({'errors': 'The requested user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_ban:
            return Response({'errors': 'The requested user is banned'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegistrationView(APIView):
    """
        Post to register an user
    """
    def __is_valid_email(self, email: str) -> bool:
        """
            Check if the email is correct
            :param email: The email being validated
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, format=None):
        """
            Post request to register an user
            :param request: The request being sent
            :param format: The format of the request
        """
        if is_user_authenticated(request):
            return Response({'errors': 'User is authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        email, password = retrieve_email_and_password(request)
        if not self.__is_valid_email(email=email):
            return Response({'errors': 'The provided email is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.create_user(email=email, password=password)
        if not user:
            return Response({'errors': 'The email already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
        Logout the user
    """
    permission_classes = (permissions.IsAuthenticated, IsNotBanned,)

    def get(self, request, fromat=None):
        """
            Logout from the API

            :param request: The request
            :param format: The format of the request
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)

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
    if is_user_authenticated(request):
        response[constants.TODO_LIST_URI_INFO][constants.METHOD_KEY] = [constants.GET_METHOD, constants.POST_METHOD]
        response[constants.LOGOUT_URI_INFO] = generate_method_information(urls_name.LOGOUT_NAME, request=request, format=format, methods=[constants.GET_METHOD])

        if is_user_admin(request):
            response[constants.USER_LIST_URI_INFO] = generate_method_information(urls_name.USER_LIST_NAME, request=request, format=format, methods=[constants.GET_METHOD, constants.POST_METHOD])
    else:
        response[constants.REGISTRATION_URI_INFO] = generate_method_information(urls_name.REGISTER_NAME, request=request, format=format, methods=[constants.POST_METHOD])
        response[constants.LOGIN_URI_INFO] = generate_method_information(urls_name.LOGIN_NAME, request=request, format=format, methods=[constants.POST_METHOD])
    return Response(response)
