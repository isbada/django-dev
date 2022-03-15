# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-13 16:02:50
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''
from django.contrib import admin
# re_path支持路径正则
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>',views.blogs_with_type,name='blogs_with_type'),
    path('', views.blog_list, name='blog_list'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]
