from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url('todo/', views.ListTodo.as_view()),
    url('todo/<int::pk>/', views.DetailTodo.as_view()),
    url('user/', views.ListUser.as_view()),
    url('user/<int::pk>', views.DetailUser.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
