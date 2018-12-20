from django.contrib import admin
from .models.docker_server_models import  Docker_Server
from .models.supervisor_server_models import Supervisor_Server
from .models.jenkins_server_models import Jenkins_Server
from .models.user_info_models import User_Info
from .models.server import Server, ServerType
# Register your models here.


admin.site.register(Supervisor_Server)
admin.site.register(Docker_Server)
admin.site.register(Jenkins_Server)
admin.site.register(User_Info)
admin.site.register(Server)
admin.site.register(ServerType)
## 管理员 root   111111