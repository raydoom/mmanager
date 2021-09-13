# coding=utf8

from django.urls import path
from app.docker import views

urlpatterns = [
    path('container_list', views.ContainerListView.as_view()),
    path('container_option', views.ContainerOptionView.as_view()),
    path('container_log', views.ContainerLog.as_view()),
    path('container_console', views.ContainerConsole.as_view()),

]
