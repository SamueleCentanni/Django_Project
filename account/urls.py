from . import views
from django.urls import re_path, path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^$', views.dashboard, name='dashboard'),
    path("password-change", auth_views.PasswordChangeView.as_view(), name='password_change'),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]