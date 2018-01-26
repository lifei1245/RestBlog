from django.contrib.auth import get_user_model
from django.db import models
from user.models import UserProfile
import datetime

# Create your models here.
User = get_user_model()


class Category(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    tittle = models.CharField(max_length=100, null=False, blank=False, help_text='标题', verbose_name='标题')
    desc = models.TextField(default="", null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间', null=True, blank=True)

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tittle[:10] if len(self.tittle) >= 10 else self.tittle[:len(self.tittle)]


class Blog(models.Model):
    tittle = models.CharField(max_length=100, null=False, blank=False, help_text='标题')
    author = models.ForeignKey(User, verbose_name='作者')
    content = models.TextField(null=False, blank=False, verbose_name='内容')
    click_num = models.IntegerField(null=False, blank=False, default=0, verbose_name='点击数')
    fav_num = models.IntegerField(null=False, blank=False, default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')
    isintroduce = models.BooleanField(default=False, verbose_name='是否推荐')
    category = models.ForeignKey(Category, verbose_name='类别', null=True, blank=True)
    image = models.ImageField(max_length=200, upload_to="blog/", null=True, blank=True)

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tittle


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='评论者')
    content = models.TextField(null=False, blank=False, verbose_name='评论内容')
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')
    blog = models.ForeignKey(Blog, verbose_name='博客', blank=True, null=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10] if len(self.content) >= 10 else self.content[:len(self.content)]
