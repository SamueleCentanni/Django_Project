from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path(r'^login/$', views.user_login, name='login'),
]