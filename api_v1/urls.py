from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from . import urls_name

urlpatterns = [
    url(r'^todo/(?P<pk>\d+)/', 
        views.DetailTodo.as_view(),
        name=urls_name.TODO_DETAIL_NAME),
    url(r'^todo/', 
        views.ListTodo.as_view(),
        name=urls_name.TODO_LIST_NAME),
    url(r'^users/(?P<pk>\d+)/', 
        views.DetailUser.as_view(),
        name=urls_name.USER_DETAIL_NAME),
    url(r'^users/', 
        views.ListUser.as_view(),
        name=urls_name.USER_LIST_NAME),
    url(r'^auth/login/',
        views.UserAuthenticationView.as_view(),
        name=urls_name.LOGIN_NAME),
    url(r'^auth/logout/',
        views.LogoutView.as_view(),
        name=urls_name.LOGOUT_NAME),
    url(r'^auth/register/',
        views.UserRegistrationView.as_view(),
        name=urls_name.REGISTER_NAME),
    url(r'',
        views.api_root,
        name=urls_name.DEFAULT_NAME),
]

urlpatterns = format_suffix_patterns(urlpatterns)
