

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib.auth.models import User

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
    return render(request, 'user/login.html', context)


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
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)