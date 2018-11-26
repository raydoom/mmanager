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
from app.views import action_log_views, directory_viewer_views, docker_server_views, jenkins_server_views, supervisor_server_views, user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls,name=admin),

    url(r'^dockerserver', docker_server_views.docker_server, name='docker_server'),
    url(r'^container_opt', docker_server_views.container_option),
    url(r'^tail_container_log', docker_server_views.tail_container_log),

    url(r'^supervisorserver', supervisor_server_views.supervisor_server, name='supervisor_server'),
    url(r'^supervisor_app_opt', supervisor_server_views.supervisor_app_option),
    url(r'^tail_supervisor_app_log', supervisor_server_views.tail_supervisor_app_log),

    url(r'^jenkinsserver', jenkins_server_views.jenkins_server, name='jenkins_server'),
    url(r'^jenkins_job_opt', jenkins_server_views.jenkins_job_opt),


    url(r'^dirviewer', directory_viewer_views.dir_viewer),
    url(r'^textviewer', directory_viewer_views.text_viewer),
    url(r'^filedownload', directory_viewer_views.file_download),

    url(r'^actionslog', action_log_views.action_log),

    url(r'^login/', user_views.login),
    url(r'^register/', user_views.register),
	url(r'^logout/', user_views.logout),
    url(r'^passwordchange/', user_views.passwordchange),
    url(r'^settings/', user_views.settings),

    url(r'', docker_server_views.docker_server),
    
]


