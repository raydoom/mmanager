# coding=utf8

from django.urls import path
from app.docker import views

urlpatterns = [
    path('container_list', views.ContainerListView.as_view()),
    path('container_option', views.ContainerOptionView.as_view()),
    path('container_log', views.container_log),
    path('container_console', views.container_console),

]
