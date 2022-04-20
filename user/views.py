

from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm, ChangeNickNameForm, BindEmailForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Profile
import string
import random
import time

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


def change_nickname(request):

    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChangeNickNameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created =  Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)

    else:
        form = ChangeNickNameForm()
    
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

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


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        # 提交绑定邮箱的请求
        bind_email_form = BindEmailForm(request.POST, request=request)
        if bind_email_form.is_valid():
            email = bind_email_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)

    else:
        # 访问页面的请求
        bind_email_form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = bind_email_form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    # send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        # 发送邮件
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        # 至少间隔30s才能再次发送验证邮件
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                'isbada@foxmail.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)