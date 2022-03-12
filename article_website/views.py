# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-13 02:34:58
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")