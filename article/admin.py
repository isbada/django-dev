from django.contrib import admin
from .models import Article
# Register your models here. 将当前应用注册到后台管理界面
admin.site.register(Article)