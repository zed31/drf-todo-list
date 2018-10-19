from django.test import TestCase, Client, RequestFactory
from . import models, urls_name, views
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

    def __execute_get_request(self, user):
        """
            Execute a get request and return the response

            :param user: The user used inside the request
            :return: An http response
        """
        request_get = self.request_factory.get(reverse(urls_name.TODO_LIST_NAME))
        request_get.user = user
        todoListView = views.ListTodo.as_view()
        response = todoListView(request_get)
        return response

    def __execute_post_request(self, requestUser, jsonTodo):
        """
            Execute a post request and return the response

            :param requestUser: The user used during the post request
            :param jsonTodo: The todo used during the post request
            :return: An Http response
        """
        request_post = self.request_factory.post(reverse(urls_name.TODO_LIST_NAME), jsonTodo)
        request_post._dont_enforce_csrf_checks = True
        request_post.user = requestUser
        todoListView = views.ListTodo.as_view()
        response = todoListView(request_post)
        return response

    def setUp(self):
        """Setup the test"""
        self.request_factory = RequestFactory()
        self.user = models.UserModel(email='toto.titi-list-view-test@epitech.eu', password='toto')
        self.admin = models.UserModel(email='admin.admin-list-view-test@gmail.com', password='admin', is_superuser=True)
        self.banned_user = models.UserModel(email='banned.banned-list-view-test@gmail.com', password='banned', is_ban=True)
        self.admin.save()
        self.user.save()
        self.banned_user.save()
        
    def test_api_can_get_todo(self):
        """Api can get the todo from the database"""
        response = self.__execute_get_request(None)
        user_response = self.__execute_get_request(self.user)
        admin_response = self.__execute_get_request(self.admin)
        banned_repsonse = self.__execute_get_request(self.banned_user)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, banned_repsonse.status_code)
        self.assertEqual(status.HTTP_200_OK, admin_response.status_code)
        self.assertEqual(status.HTTP_200_OK, user_response.status_code)
    
    def test_api_can_post_todo(self):
        """Api can post a todo by being connected"""
        self.admin.save()
        self.user.save()
        self.banned_user.save()
        response_forbidden = self.__execute_post_request(None, {'title': 'test', 'description': 'test'})
        response_forbidden_banned_user = self.__execute_post_request(self.banned_user, {'title': 'test', 'description': 'test'})
        response_admin_ok = self.__execute_post_request(self.admin, {'title': 'test', 'description': 'test'})
        response_ok = self.__execute_post_request(self.user, {'title': 'test', 'description': 'test'})

        self.assertEqual(status.HTTP_403_FORBIDDEN, response_forbidden.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response_forbidden_banned_user.status_code)
        self.assertEqual(status.HTTP_201_CREATED, response_ok.status_code)
        self.assertEqual(status.HTTP_201_CREATED, response_admin_ok.status_code)
    
class TodoDetailView(TestCase):
    """Test case used to test the todo detail view"""

    def __execute_get_request(self, todo, user):
        """
            Execute a get request and return the response

            :param todo: The todo used for the request
            :param user: The user used for the request
            :return: the http response
        """
        request_get = self.request_factory.get(reverse(urls_name.TODO_DETAIL_NAME, kwargs={'pk': todo.id}))
        request_get.user = user
        detail = views.DetailTodo.as_view()
        todo_response = detail(request_get, pk=todo.id)
        return todo_response
    
    def __execute_put_request(self, todo, modification, user):
        """
            Execute a put request and return the response

            :param todo: The todo used for the request
            :param user: The user used for the request
            :return: The Http reponse
        """
        request_put = self.request_factory.put(reverse(urls_name.TODO_DETAIL_NAME, kwargs={'pk': todo.id}), modification, content_type='application/json')
        request_put.user = user
        request_put._dont_enforce_csrf_checks = True
        detail = views.DetailTodo.as_view()
        return detail(request_put, pk=todo.id)

    def __execute_delete_command(self, todo, user):
        """
            Execute a delete command and return the response

            :param todo: The todo used for the request
            :param user: The user used for the request
        """
        request_delete = self.request_factory.delete(reverse(urls_name.TODO_DETAIL_NAME, kwargs={'pk': todo.id}))
        request_delete.user = user
        request_delete._dont_enforce_csrf_checks = True
        detail = views.DetailTodo.as_view()
        return detail(request_delete, pk=todo.id)

    def setUp(self):
        """Setup the test"""
        self.request_factory = RequestFactory()
        self.user = models.UserModel(email='toto.titi@tutu.com', password='test')
        self.user_banned = models.UserModel(email='banned.user@gmail.com', password='test', is_ban=True)
        self.admin = models.UserModel(email='admin.api@test.com', password='admin', is_superuser=True)
        self.admin.save()
        self.user.save()
        self.user_banned.save()
        self.todo = models.TodoListModel(title='test', description='test description', owner=self.user)
        self.admin_todo = models.TodoListModel(title='admin todo test', description='admin todo test description', owner=self.admin)
        self.banned_todo = models.TodoListModel(title='todo made by a banned user', description='todo made by a banned user', owner=self.user_banned)
        self.todo.save()
        self.admin_todo.save()
        self.banned_todo.save()

    def test_api_can_delete_todo(self):
        """Test case that check if we can delete the todos"""
        todo_by_user = models.TodoListModel(title='test to remove', description='test descritpion to remove', owner=self.user)
        todo_by_user_removed_by_admin = models.TodoListModel(title='test to remove', description='test descritpion to remove', owner=self.user)
        todo_by_admin = models.TodoListModel(title='test to remove', description='todo from the admin to remove', owner=self.admin)
        todo_by_banned_user = models.TodoListModel(title='test to remove', description='todo from the admin to remove', owner=self.admin)
        todo_by_user.save()
        todo_by_user_removed_by_admin.save()
        todo_by_admin.save()
        todo_by_banned_user.save()

        removed_user_todo = self.__execute_delete_command(todo=todo_by_user, user=self.user)
        removed_admin_todo_forbidden = self.__execute_delete_command(todo=todo_by_admin, user=self.user)
        removed_admin_todo_user = self.__execute_delete_command(todo=todo_by_user_removed_by_admin, user=self.admin)
        removed_task_by_banned_user_forbidden = self.__execute_delete_command(todo=todo_by_banned_user, user=self.user_banned)
        removed_non_existent_todo = self.__execute_delete_command(todo=todo_by_user, user=self.user)

        self.assertEqual(status.HTTP_204_NO_CONTENT, removed_user_todo.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, removed_admin_todo_forbidden.status_code)
        self.assertEqual(status.HTTP_204_NO_CONTENT, removed_admin_todo_user.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, removed_task_by_banned_user_forbidden.status_code)
        self.assertEqual(status.HTTP_404_NOT_FOUND, removed_non_existent_todo.status_code)
    
    def test_api_can_get_detail_of_a_todo(self):
        """Test if we can get a detail of a todo"""
        todo = models.TodoListModel.objects.get(owner__email='toto.titi@tutu.com')
        todo_admin = models.TodoListModel.objects.get(owner__email='admin.api@test.com')
        todo_response = self.__execute_get_request(todo, self.user)
        todo_admin_response = self.__execute_get_request(todo_admin, self.user)
        todo_banned_response = self.__execute_get_request(todo, self.user_banned)
        todo_admin_right_check_response = self.__execute_get_request(todo, self.admin)
        todo_banned_user_access_to_todo_response = self.__execute_get_request(self.banned_todo, self.user_banned)

        self.assertEqual(status.HTTP_403_FORBIDDEN, todo_banned_response.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, todo_admin_response.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, todo_banned_user_access_to_todo_response.status_code)
        self.assertEqual(status.HTTP_200_OK, todo_response.status_code)
        self.assertEqual(status.HTTP_200_OK, todo_admin_right_check_response.status_code)
    
    def test_api_can_put_detail_of_a_todo(self):
        """Test if we can put detail of a todo"""
        user_modification_response = self.__execute_put_request(self.todo, {'title': 'Modified by user', 'description': self.todo.description}, self.user)
        updated_todo_queryset = models.TodoListModel.objects.filter(id=self.todo.id)
        updated_todo = updated_todo_queryset.get()
        user_modification_ill_formed_response = self.__execute_put_request(self.todo, {'title': 'Modified by user'}, self.user)
        user_modification_on_another_task = self.__execute_put_request(self.admin_todo, {'title': 'Modified by user', 'description': 'Description modified by user'}, self.user)

        admin_modification_response = self.__execute_put_request(self.todo, {'title': 'Modified by the admin', 'description': 'Description modified by the admin'}, self.admin)
        updated_todo_admin_queryset = models.TodoListModel.objects.filter(id=self.todo.id)
        updated_todo_admin = updated_todo_admin_queryset.get()

        banned_forbidden_modification = self.__execute_put_request(self.banned_todo, {'title': 'modified by a banned user', 'description': self.banned_todo.description}, self.user_banned)
        updated_todo_banned_queryset = models.TodoListModel.objects.filter(id=self.banned_todo.id)
        updated_todo_banned = updated_todo_banned_queryset.get()
        
        self.assertEqual(status.HTTP_200_OK, user_modification_response.status_code)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, user_modification_ill_formed_response.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, user_modification_on_another_task.status_code)
        self.assertEqual(status.HTTP_403_FORBIDDEN, banned_forbidden_modification.status_code)
        self.assertEqual(status.HTTP_200_OK, admin_modification_response.status_code)
    
