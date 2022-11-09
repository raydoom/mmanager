# coding=utf8

from django.urls import path
from app.main import views

urlpatterns = [
    path('index', views.IndexView.as_view()),

]
