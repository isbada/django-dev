# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-13 02:34:58
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''

from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    return HttpResponse("Hello, world!")


def home(request):
    context = {}
    return render_to_response('home.html', context)
