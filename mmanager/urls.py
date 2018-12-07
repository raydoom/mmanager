from django.conf.urls import url
from django.contrib import admin
from app.views import ( action_log_views, directory_viewer_views, 
                        docker_server_views, jenkins_server_views, 
                        supervisor_server_views, user_views,
                        server_list_views

                      )

urlpatterns = [
    url(r'^admin/', admin.site.urls,name=admin),

    url(r'^dockerserver', docker_server_views.Docker_Server_List.as_view(), name='docker_server_list'),
    url(r'^container_opt', docker_server_views.Container_Option.as_view(), name='container_option'),
    url(r'^tail_container_log', docker_server_views.Tail_Container_Log.as_view(), name='tail_container_log'),

    url(r'^supervisorserver', supervisor_server_views.Supervisor_Server_List.as_view(), name='supervisor_server'),
    url(r'^supervisor_app_opt', supervisor_server_views.Supervisor_App_Option.as_view(), name='supervisor_app_opt'),
    url(r'^tail_supervisor_app_log', supervisor_server_views.Tail_Supervisor_App_Log.as_view(), name='tail_supervisor_app_log'),

    url(r'^jenkinsserver', jenkins_server_views.Jenkins_Server_List.as_view(), name='jenkins_server'),
    url(r'^jenkins_job_opt', jenkins_server_views.Jenkins_Job_Opt.as_view(), name='jenkins_job_opt'),


    url(r'^dirviewer', directory_viewer_views.Directory_Viewer.as_view(), name='directory_viewer'),
    url(r'^textviewer', directory_viewer_views.Text_Viewer.as_view(), name='text_viewer'),
    url(r'^filedownload', directory_viewer_views.File_Download.as_view(), name='file_download'),

    url(r'^actionlog', action_log_views.Action_Log_List.as_view(), name='action_log_list'),

    url(r'^login/', user_views.Login.as_view(), name='login'),
    url(r'^register/', user_views.Register.as_view(), name='register'),
	url(r'^logout/', user_views.Sign_Out.as_view(), name='sign_out'),
    url(r'^changepassword/', user_views.Change_Password.as_view(), name='change_password'),
    url(r'^account/', user_views.Account.as_view(), name='account'),
    url(r'^serverlist/', server_list_views.Server_List.as_view(), name='server_list'),
    url(r'^users/', user_views.Users.as_view(), name='users'),
    url(r'^createuser/', user_views.Create_User.as_view(), name='create_user'),
    url(r'^deleteuser/', user_views.Delete_User.as_view(), name='delete_user'),

    url(r'^addserver/', server_list_views.Add_Server.as_view(), name='add_server'),
    url(r'^deleteserver/', server_list_views.Delete_Server.as_view(), name='delete_server'),


    url(r'', docker_server_views.Docker_Server_List.as_view(), name='default'),
    
]


