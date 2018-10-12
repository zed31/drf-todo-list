from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class TodoListModel(models.Model):
    """
        Describe the model of a Task and generate an ORM
    """
    STATUS_CHOICE = [
        ('C', 'Created'), ('P', 'In progress'), ('D', 'Done')
    ]

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE, default='Created', max_length=100)

    class Meta:
        """
            Some optional field like ordering to sort the table
        """
        ordering = ('created',)

class UserManager(BaseUserManager):
    """
        The user manager used by django to create users
        as well as staff and super user
    """
    use_in_migration = True

    def __save_and_return(self, user, password: str, is_staff: bool, is_admin: bool):
        """
            Save the user inside the database by setting some values and
            using the default database

            :param user: The user model
            :param password: The stored password
            :param is_staff: boolean field to know if it's a staff user
            :param is_admin: boolean field to know if the user is an administrator
        """
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: models.EmailField, password: str=None):
        """
            Create an user
            :param email: the email field
            :param password: the password field
        """
        user = self.model(email=self.normalize_email(email))
        return self.__save_and_return(user=user, password=password, is_admin=False, is_staff=False)
    
    def create_staffuser(self, email: models.EmailField, password: str):
        """
            Create an user
            :param email: the email field
            :param password: the password field
        """
        user = self.create_user(email=email, password=password)
        return self.__save_and_return(user=user, password=password, is_admin=False, is_staff=True)
    
    def create_superuser(self, email: models.EmailField, password: str):
        """
            Create an user
            :param email: the email field
            :param password: the password field
        """
        user = self.create_user(email=email, password=password)
        return self.__save_and_return(user=user, password=password, is_admin=True, is_staff=True)

class UserModel(AbstractBaseUser):
    """
        Define the model of the user
    """
    objects = UserManager()

    username = None
    email = models.EmailField(('email address'), unique=True)
    is_ban = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

