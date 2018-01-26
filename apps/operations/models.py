from django.contrib.auth import get_user_model
from django.db import models
from blog.models import Blog, Comment
import datetime

User = get_user_model()


# Create your models here.


class FavBlog(models.Model):
    """
    收藏操作
    """
    blog = models.ForeignKey(Blog, verbose_name='博客')
    user = models.ForeignKey(User, verbose_name='用户')
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')
