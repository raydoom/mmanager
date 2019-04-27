# coding=utf8

from django.urls import path
from app.action_log import views

urlpatterns = [
    path('action_log_list', views.ActionLogListView.as_view()),

]
