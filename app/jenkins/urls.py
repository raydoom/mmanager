# coding=utf8

from django.urls import path
from app.jenkins import views

urlpatterns = [
    path('job_list', views.JobListView.as_view()),
    path('job_option', views.JobOptionView.as_view()),

]
