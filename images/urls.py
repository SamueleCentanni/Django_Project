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
    path('create_local/', views.image_create_local, name='create_local'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('', views.image_list, name='list'),
    path('ranking/', views.image_ranking, name='ranking'),
    path('images/image_list/', views.user_image_list, name='your_images'),
    path('delete/<int:pk>/', views.ImageDeleteView.as_view(), name='delete'),
]
