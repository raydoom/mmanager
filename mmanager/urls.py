# urls.py

from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib import admin
from app.views import (  directory_viewer_views, 
                         jenkins_server_views, 
                       
                      )

urlpatterns = [
    url(r'^admin/', admin.site.urls,name=admin),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),

    url(r'^jenkinsserver/', jenkins_server_views.Jenkins_Server_List.as_view(), name='jenkins_server'),
    url(r'^jenkins_job_opt/', jenkins_server_views.Jenkins_Job_Opt.as_view(), name='jenkins_job_opt'),


    url(r'^directoryviewer/', directory_viewer_views.Directory_Viewer.as_view(), name='directory_viewer'),
    url(r'^textviewer/', directory_viewer_views.Text_Viewer.as_view(), name='text_viewer'),
    url(r'^filedownload/', directory_viewer_views.File_Download.as_view(), name='file_download'),

    path('account/', include('app.account.urls')),
    path('server/', include('app.server.urls')),
    path('docker/', include('app.docker.urls')),
    path('supervisor/', include('app.supervisor.urls')),
    path('action_log/', include('app.action_log.urls')),
    
]


