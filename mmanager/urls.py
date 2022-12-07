# urls.py

from django.urls import re_path as url
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls,name=admin),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),

    path('index/', include('app.main.urls')),
    path('account/', include('app.account.urls')),
    path('server/', include('app.server.urls')),
    path('docker/', include('app.docker.urls')),
    path('supervisor/', include('app.supervisor.urls')),
    path('jenkins/', include('app.jenkins.urls')),
    path('filemanager/', include('app.filemanager.urls')),
    path('action_log/', include('app.action_log.urls')),

    url(r'^', RedirectView.as_view(url='/account/login')),
    
]


