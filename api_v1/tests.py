from django.test import TestCase, Client
from . import models, urls_name
from rest_framework.reverse import reverse
from rest_framework import status
from django.db import transaction

# Create your tests here.
class UserTestCase(TestCase):
    """This class test the user model"""
    def setUp(self):
        """Define the test client and other tests variables"""
        self.user_email = 'foo.bar@gmail.com'
        self.user_password = 'lb/n2dcx'
        self.user_model = models.UserModel(email=self.user_email, password=self.user_password)
    
    def test_model_can_create_user(self):
        """Check if the model can create new users"""
        old_count = models.UserModel.objects.count()
        self.user_model.save()
        new_count = models.UserModel.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertGreater(new_count, old_count)
        self.assertEqual(0, old_count)

    def test_model_can_retrieve_user(self):
        """Check if the user can be retrieved through his email"""
        new_user = models.UserModel(email='bar.foo@epitech.eu', password='toto')
        new_user.save()
        retrieved_new_user = models.UserModel.objects.get(email='bar.foo@epitech.eu')
        self.assertEqual(1, models.UserModel.objects.count())
        self.assertEqual('bar.foo@epitech.eu', retrieved_new_user.email)
    
    def test_model_can_remove_user(self):
        """Check if the user can be removed"""
        foo_bar = models.UserModel(email='foo.bar@epitech.eu', password='toto')
        bar_foo = models.UserModel(email='bar.foo@epitech.eu', password='tutu')
        other = models.UserModel(email='lala.lulu@epitech.eu', password='lalalulu')
        foo_bar.save()
        bar_foo.save()
        other.save()
        self.assertEqual(3, models.UserModel.objects.count())
        foo_bar_retrieved = models.UserModel.objects.get(email='foo.bar@epitech.eu')
        self.assertEqual('foo.bar@epitech.eu', foo_bar_retrieved.email)
        foo_bar_retrieved.delete()
        self.assertEqual(2, models.UserModel.objects.count())
    
    def test_model_can_update_user(self):
        """Check if model can update the user"""
        new_user = models.UserModel(email='bar.foo@epitech.eu', password='toto')
        foo_bar = models.UserModel(email='foo.bar@epitech.eu', password='toto')
        other = models.UserModel(email='lala.lulu@epitech.eu', password='lalalulu')
        new_user.save()
        foo_bar.save()
        other.save()
        self.assertEqual(3, models.UserModel.objects.count())
        queryset_new_user = models.UserModel.objects.filter(email__startswith='foo.bar@epitech')
        queryset_change_email = models.UserModel.objects.filter(email__startswith='bar.foo')
        self.assertEqual(1, queryset_new_user.count())
        self.assertEqual(1, queryset_change_email.count())
        queryset_new_user.update(is_ban=True)
        queryset_change_email.update(email='lulu.lala@epitech.eu')
        updated_email_user = models.UserModel.objects.get(email='lulu.lala@epitech.eu')
        updated_user = models.UserModel.objects.get(email='foo.bar@epitech.eu')
        self.assertEqual(True, updated_user.is_ban)
        self.assertEqual('lulu.lala@epitech.eu', updated_email_user.email)

class AuthTest(TestCase):
    """Test case used to test the authentication and registration"""
    def setUp(self):
        """Setup the tests"""
        self.user = models.UserModel(email='toto.titi@epitech.eu', password='toto')
        self.banned_user = models.UserModel(email='titi.toto@epitech.eu', password='test', is_ban=True)
    
    def test_api_can_signin_user(self):
        """Test if the user can authenticate with the api"""
        self.user.save()
        self.banned_user.save()
        response = self.client.post(reverse(urls_name.LOGIN_NAME), {'email': self.user.email, 'password': self.user.password})
        response_is_ban = self.client.post(reverse(urls_name.LOGIN_NAME), {'email': self.banned_user.email, 'password': self.banned_user.password})
        response_unknown_user = self.client.post(reverse(urls_name.LOGIN_NAME), {'email': 'unknown.user@epitech.eu', 'password': 'unknown'})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_is_ban.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_unknown_user.status_code)
    
    def test_api_can_register_user(self):
        """Test if the API can register an user"""
        self.user.save()

        response = self.client.post(reverse(urls_name.REGISTER_NAME), {'email': 'test.register@gmail.com', 'password': 'test-password'})
        response_user_already_exist = self.client.post(reverse(urls_name.REGISTER_NAME), {'email': self.user.email, 'password': self.user.password})
        response_user_email_invalid = self.client.post(reverse(urls_name.REGISTER_NAME), {'email': 'bad-email', 'password': 'unknown'})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_user_already_exist.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_user_email_invalid.status_code)
    
    def test_api_can_logout_user(self):
        """Test the logout action of the API"""
        self.user.save()

        login_response = self.client.post(reverse(urls_name.LOGIN_NAME), {'email': self.user.email, 'password': self.user.password})
        response_logout = self.client.get(reverse(urls_name.LOGOUT_NAME))
        response_logout_without_auth = self.client.get(reverse(urls_name.LOGOUT_NAME))

        self.assertEqual(status.HTTP_200_OK, login_response.status_code)
        self.assertEqual(status.HTTP_200_OK, response_logout.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_logout_without_auth.status_code)



class TodoListView(TestCase):
    """Test case used to test the todo list view"""
    def setUp(self):
        """Setup the test"""
        self.user = models.UserModel(email='toto.titi@epitech.eu', password='toto')

    def test_api_can_get_todo(self):
        """Api can get the todo from the database"""
        self.user.save()
        sample_todo = models.TodoListModel(title='nourrir le chien', description='nourrir le chien', owner=self.user)
        sample_todo.save()
        response = self.client.get(reverse(urls_name.TODO_LIST_NAME))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_can_post_todo(self):
        """Api can post a todo by being connected"""
        self.user.save()
        response_forbidden = self.client.post(reverse(urls_name.TODO_LIST_NAME), {'title': 'test', 'description': 'test'})
        login_response = self.client.post(reverse(urls_name.LOGIN_NAME), {'email': self.user.email, 'password': self.user.password})
        response = self.client.post(reverse(urls_name.TODO_LIST_NAME), {'title': 'test', 'description': 'test'})

        self.assertEqual(status.HTTP_403_FORBIDDEN, response_forbidden.status_code)
        self.assertEqual(status.HTTP_200_OK, login_response.status_code)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
