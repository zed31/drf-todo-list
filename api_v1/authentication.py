from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackendModel(ModelBackend):
    """
        Backend used to authenticate users and
        helps generate the session id
    """
    def authenticate(self, username=None, password=None, **kwargs):
        """
            authenticate the user by retrieving it from the
            database

            :param username: The username of the user
            :param password: The password of the user
            :param kwargs: Other cool stuff you can add
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            return user
        except UserModel.DoesNotExist:
            return None