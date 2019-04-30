# coding=utf8

from django.contrib import admin
from app.account.models import User
from app.server.models import Server, ServerType
# Register your models here.


admin.site.register(User)
admin.site.register(Server)
admin.site.register(ServerType)
## 管理员 root   111111