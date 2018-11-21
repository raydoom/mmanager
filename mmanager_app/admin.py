from django.contrib import admin
from .models.docker_server import  Docker_Server
from .models.supervisor_server import Supervisor_Server
from .models.jenkins_server import Jenkins_Server
# Register your models here.


admin.site.register(Supervisor_Server)
admin.site.register(Docker_Server)
admin.site.register(Jenkins_Server)


## 管理员 ma   111111