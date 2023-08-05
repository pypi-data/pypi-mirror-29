from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views
from django_openid_auth import views as auth_view


urlpatterns = [
    url(r'^api-auth/openid/login/$', csrf_exempt(auth_view.login_begin), name='openid-login'),
    url(r'^api-auth/openid/complete/$', auth_view.login_complete, name='openid-complete'),
    url(r'^api-auth/openid/logo.gif$', auth_view.logo, name='openid-logo'),
    url(r'^api-auth/openid/login_completed/', views.login_completed),
]
