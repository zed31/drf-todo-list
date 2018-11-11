from .authentication import EmailBackendModel
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.cache import cache
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import request_utils
from . import models

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
        cache.set(request.session.session_key, user.email, 60*60*24)
        serializer = UserSerializer(user, context={'request': request})
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
        if request_utils.is_user_authenticated(request):
            return Response({'errors': 'User is authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        email, password = retrieve_email_and_password(request)
        if not self.__is_valid_email(email=email):
            return Response({'errors': 'The provided email is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        user = models.UserModel.objects.create_user(email=email, password=password)
        if not user:
            return Response({'errors': 'The email already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
        Logout the user
    """
    def get(self, request, fromat=None):
        """
            Logout from the API

            :param request: The request
            :param format: The format of the request
        """
        if not request_utils.is_user_authenticated(request):
            return Response({'errors': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        cache.delete(request.session.session_key)
        logout(request)
        return Response(status=status.HTTP_200_OK)
