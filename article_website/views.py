# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-13 02:34:58
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''

import imp
from importlib.metadata import requires
from django.http import HttpResponse,JsonResponse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.shortcuts import render, redirect
import datetime
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib.auth.models import User


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]


def index(request):
    return HttpResponse("Hello, world!")


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取七天热门博客的缓存数据
    hot_data_for_7days = cache.get('hot_data_for_7days')
    if hot_data_for_7days is None:
        hot_data_for_7days = get_7_days_hot_blogs()
        cache.set('hot_data_for_7days', hot_data_for_7days, 3600)
        print('calculate cache')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_data_for_7days'] = get_7_days_hot_blogs()

    return render(request, 'home.html', context)


def login(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER', reverse('home'))

    # if user is not None:
    #     auth.login(request, user)
    #     # redirect a login page
    #     return redirect(referer)

    # else:
    #     # return an invalid page
    #     return render(request, 'error.html', {'message': '用户名或者密码不正确'})

    if request.method == 'POST':
        # 提交登录信息的请求
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 验证通过
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            # redirect a login page
            return redirect(request.GET.get('from', reverse('home')))

    else:
        # 访问页面的请求
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        # 提交登录信息的请求
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            # 验证通过,创建用户
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        # 访问页面的请求
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)