from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',verbose_name='昵称')
    nickname = models.CharField(max_length=20, default='')


    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)