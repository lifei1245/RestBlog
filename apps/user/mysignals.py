# coding=utf-8
# @Time : 2018/1/8 15:30
# @Author : 李飞
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
