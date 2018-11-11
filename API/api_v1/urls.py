from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from . import urls_name, urls_auth

urlpatterns = [
    url(r'^me/todo/',
        views.MeTodo.as_view(),
        name=urls_name.ME_TODO),
    url(r'^admin/todo/',
        views.CreateAdminTodo.as_view(),
        name=urls_name.ME_TODO),
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
]

urlpatterns += urls_auth.urlpatterns
urlpatterns += [
    url(r'',
        views.api_root,
        name=urls_name.DEFAULT_NAME),
]

urlpatterns = format_suffix_patterns(urlpatterns)
