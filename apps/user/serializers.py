# coding=utf-8
# @Time : 2018/1/19 14:59
# @Author : 李飞
from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

from rest_framework.validators import UniqueValidator

from RestBlog.settings import PHONE_REG
from datetime import datetime, timedelta
from .models import VerifyCodeModel, UserProfile

User = get_user_model()


class SmsSendSerializer(serializers.Serializer):
    mobile = serializers.CharField(min_length=11, required=True, allow_blank=False, help_text='手机号码')

    def validate_mobile(self, mobile):
        user = User.objects.filter(mobile=mobile)
        if user:
            raise serializers.ValidationError('已经注册')
        if not re.match(PHONE_REG, mobile):
            raise serializers.ValidationError('手机帐号格式错误')
        on_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCodeModel.objects.filter(mobile=mobile, add_time__gt=on_minute_ago):
            raise serializers.ValidationError('验证码发送太快')
        return mobile

    def __str__(self):
        return self.mobile


class UserRegsterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, min_length=6, max_length=6, required=True, help_text='验证码',
                                 error_messages={
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                     'allow_blank': '请输入验证码',
                                 })
    mobile = serializers.CharField(min_length=11, max_length=11, required=True, help_text='手机',
                                   validators=[
                                       UniqueValidator(queryset=User.objects.all(), message='用户已存在')
                                   ])
    password = serializers.CharField(write_only=True, style={
        'input_type': 'password'
    }, label='密码', allow_blank=False, required=True)

    def validate_code(self, code):
        m = VerifyCodeModel.objects.filter(mobile=self.initial_data['mobile']).order_by('-add_time')
        if m:
            record_code = m[0]
            one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if record_code.add_time < one_minute_ago:
                raise serializers.ValidationError('验证码过期')
            if record_code.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs['username'] = attrs['mobile']
        del attrs['code']
        return attrs

    class Meta:
        model = UserProfile
        fields = ('mobile', 'code', 'password')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'id', 'name', 'mobile', 'image', 'gender', 'email')


class ChangePasswordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    password = serializers.CharField(write_only=True, help_text='密码')

    class Meta:
        model = User
        fields = ('user', 'password')
