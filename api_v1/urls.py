from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^todo/(?P<pk>\d+)/', 
        views.DetailTodo.as_view(),
        name='todo-detail'),
    url(r'^todo/', 
        views.ListTodo.as_view(),
        name='todo-list'),
    url(r'^users/(?P<pk>\d+)/', 
        views.DetailUser.as_view(),
        name='user-detail'),
    url(r'^users/', 
        views.ListUser.as_view(),
        name='user-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
