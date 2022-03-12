from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)  # 文本型
    content = models.TextField() # 长文本