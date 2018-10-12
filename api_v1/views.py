from rest_framework import generics, permissions
from .serializers import TodoListSerializer, UserSerializer
from .models import TodoListModel, UserModel
from .permissions import IsOwnerOrAdminOrReadOnly
from .authentication import EmailBackendModel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import status

# Create your views here.
class ListTodo(generics.ListCreateAPIView):
    """
        List all the todo present inside the database
        also allows POST request to create some
    """
    queryset = TodoListModel.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly,)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly,)

class ListUser(generics.ListCreateAPIView):
    """
        List all users from the database
        also allows POST request to create some
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly,)

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    """
        Detail the specific user from the database
        also allows the update and the destroy of this
        specific user
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly,)

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
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        authentication_backend = EmailBackendModel()
        user = authentication_backend.authenticate(username=email, password=password)
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user.is_ban:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response(status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
        Logout the user
    """
    permission_classes = (permissions.IsAuthenticated,)

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
