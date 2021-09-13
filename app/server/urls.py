# coding=utf8

from django.urls import path
from app.server import views

urlpatterns = [
    path('server_list', views.ServerListView.as_view()),
    path('server_create', views.ServerCreateView.as_view()),
    path('server_update', views.ServerUpdateView.as_view()),
    path('server_delete', views.ServerDeleteView.as_view()),

]