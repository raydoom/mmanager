# coding=utf8

from django.urls import path
from app.filemanager import views

urlpatterns = [
    path('directory_list', views.DirectoryListView.as_view()),
    path('text_viewer', views.TextViewerView.as_view()),
    path('file_download', views.FileDownloadView.as_view()),

]
