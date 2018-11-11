from . import registration_views
from django.conf.urls import url, include
from . import urls_name

urlpatterns = [
    url(r'^auth/login/',
        registration_views.UserAuthenticationView.as_view(),
        name=urls_name.LOGIN_NAME),
    url(r'^auth/logout/',
        registration_views.LogoutView.as_view(),
        name=urls_name.LOGOUT_NAME),
    url(r'^auth/register/',
        registration_views.UserRegistrationView.as_view(),
        name=urls_name.REGISTER_NAME),
]