from rest_framework import generics, permissions
from .serializers import TodoListSerializer, UserSerializer
from .models import TodoListModel, UserModel
from .permissions import IsOwnerOrAdminOrReadOnly, IsAdmin, IsNotBanned
from .authentication import EmailBackendModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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

def retrieve_email_and_password(request):
    """
        Extract the email and the password from a request

        :param request: The request
    """
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    return email, password

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
        return Response(status=status.HTTP_200_OK)

class UserRegistrationView(APIView):
    """
        Post to register an user
    """
    def is_valid_email(self, email: str) -> bool:
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
        if request.session.session_key:
            return Response({'errors': 'User is authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        email, password = retrieve_email_and_password(request)
        if not self.is_valid_email(email=email):
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

@api_view(['GET', 'POST'])
def api_root(request, format=None):
    """
        This response is returned each time a root is not found just to show
        to the user the different root he can go to
    """
    return Response({
        'todo': reverse('todo-list', request=request, format=format),
        'user': reverse('user-list', request=request, format=format),
        'login': reverse('login-view', request=request, format=format),
    })
