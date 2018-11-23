"""maops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mmanager_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls,name=admin),
    url(r'^dockerserver', views.docker_server, name='docker_server'),
    url(r'^container_opt', views.container_option),
    url(r'^tail_container_log', views.tail_container_log),

    url(r'^supervisorserver', views.supervisor_server, name='supervisor_server'),
    url(r'^supervisor_app_opt', views.supervisor_app_option),
    url(r'^tail_supervisor_app_log', views.tail_supervisor_app_log),

    url(r'^jenkinsserver', views.jenkins_server, name='jenkins_server'),
    url(r'^jenkins_job_opt', views.jenkins_job_opt),


    url(r'^dirviewer', views.dir_viewer),
    url(r'^textviewer', views.text_viewer),
    url(r'^filedownload', views.file_download),

    url(r'^actionslog', views.actions_log),

    url(r'^login/', views.login),
    url(r'^register/', views.register),
	url(r'^logout/', views.logout),

    url(r'', views.docker_server),
    
]


