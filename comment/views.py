from django.shortcuts import render
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse


# Create your views here.
def update_comment(request):
    user = request.user
    text = request.POST.get('text', '')
    content_type = request.POST.get('content_type', '')
    object_id = int(request.POST.get('object_id', ''))
    model_class = ContentType.objects.get(model=content_type).model_class()
    model_obj = model_class.objects.get(pk=object_id)

    comment = Comment()
    comment.user = user
    comment.text = text
    # Blog.objects.get(pk=object_id)
    comment.content_object = model_obj
    comment.save()

    referer = request.META.get('HTTP_REFERER', reverse('home'))
    return redirect(referer)
