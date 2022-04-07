from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Comment(models.Model):
    
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments',on_delete=models.DO_NOTHING)

    
    root = models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING,related_name='root_comment')
    # 关联到上一级的对象  parent_id = models.IntegerField(default=0)
    parent = models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING,related_name='parent_comment')
    reply_to = models.ForeignKey(User,related_name='replies',on_delete=models.DO_NOTHING,null=True)

    class Meta:
        ordering = ['comment_time']

    def __str__(self):
        return self.text

