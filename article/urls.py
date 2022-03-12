# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-13 03:31:56
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''


# re_path支持路径正则
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<int:article_id>', views.article_detail, name='article_detail'),
    path('', views.article_list, name='article_list'),
]
    