# coding=utf8

from django.urls import path
from app.supervisor import views

urlpatterns = [
    path('process_list', views.ProcessListView.as_view()),
    path('process_option', views.ProcessOptionView.as_view()),
    path('process_log', views.process_log),

]