from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
]