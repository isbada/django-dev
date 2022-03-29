# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-20 03:31:06
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''

# re_path支持路径正则
from django.urls import path
from . import views

urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
]
