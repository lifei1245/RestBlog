from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


# Create your models here.

class UserProfile(AbstractUser):
    """
    用户
    """
    GENDER = (("male", u"男"), ("female", "女"))
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名", help_text='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月", help_text='出生日期')
    gender = models.CharField(max_length=6, choices=GENDER, default="female",
                              verbose_name="性别", help_text='性别')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话", help_text='电话')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱", help_text='邮箱')
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')
    image = models.ImageField(max_length=200, upload_to="avater/", null=True, blank=True, verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCodeModel(models.Model):
    code = models.CharField(blank=True, null=True, max_length=6, verbose_name='验证码', help_text='验证码')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    MessageType = (
        ('blog', '博客留言'),
        ('system', '系统消息')
    )
    msg = models.TextField(verbose_name='信息', help_text='信息')
    isread = models.BooleanField(verbose_name='是否已读', help_text='是否已读')
    user = models.ForeignKey(UserProfile, verbose_name='用户', help_text='用户')
    type = models.CharField(max_length=6, choices=MessageType, verbose_name='消息类别', help_text='消息类别')
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
