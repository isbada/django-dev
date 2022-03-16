# -*- coding:utf-8 -*-
'''
Author: maydayfu
Date: 2022-03-17 02:23:42
LastEditors: maydayfu
Description: 
Copyright 2021 Tencent All rights reserved.
'''

from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = f"{ct.model}_{obj.pk}_read"
    if not request.COOKIES.get(key):

        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在记录
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

    return key