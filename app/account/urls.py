# coding=utf8

from django.urls import path
from app.account import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
	path('logout', views.LogoutView.as_view()),
    path('password_change', views.PasswordChangeView.as_view()),
    path('password_reset', views.PasswordResetView.as_view()),
    path('my_account', views.MyAccountView.as_view()),
    path('user_list', views.UserListView.as_view()),
    path('user_create', views.UserCreateView.as_view()),
    path('user_delete', views.UserDeleteView.as_view()),

]
