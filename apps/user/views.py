from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from RestBlog.settings import SMS_APIKEY
from user.serializers import SmsSendSerializer, UserRegsterSerializer, UserDetailSerializer, \
    ChangePasswordSerializer
from util.yunpian import YunPian
from .models import VerifyCodeModel


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            User = get_user_model()
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


class SmsSendViewSet(GenericViewSet, CreateModelMixin):
    """
    create:
        发送验证码
    """
    serializer_class = SmsSendSerializer

    def gen_code(self):
        seeds = '1234567890'
        s = []
        for i in range(6):
            s.append(choice(seeds))
        return ''.join(s)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        yunpian = YunPian(SMS_APIKEY)
        code = self.gen_code()
        r = yunpian.send_single_sms(code, mobile)
        if r.json()['code'] != 0:
            return Response({
                'mobile': r.json()['detail']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            verifycode = VerifyCodeModel(mobile=mobile, code=code)
            verifycode.save()
            return Response({
                'mobile': mobile,
                'code': code
            }, status=status.HTTP_201_CREATED)


class ChangePassWord(GenericViewSet, UpdateModelMixin):
    serializer_class = ChangePasswordSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(serializer.initial_data['password'])
        user.save()


class UserView(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """
    create:
        新增用户
    retrieve:
        用户详情(注意只需要将url拼成这种格式,只能获取当前登录用户的信息,id随便传什么都无所谓)
    update:
        部分更新用户资料(注意只需要将url拼成这种格式,只能修改当前登录用户的信息,id随便传什么都无所谓)
    partial_update:
        全部部分更新用户资料(注意只需要将url拼成这种格式,只能修改当前登录用户的信息,id随便传什么都无所谓,此接口慎用,因为如果未传的字段会被全部置空)
    """
    User = get_user_model()
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegsterSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_object(self):
        return self.request.user

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    # def get_authenticators(self):
    #     if self.action_map['get'] == 'create':
    #         return []
    #     elif self.action_map['get'] == 'retrieve':
    #         return [JSONWebTokenAuthentication(), SessionAuthentication()]
    #     return [JSONWebTokenAuthentication(), SessionAuthentication()]

    def perform_create(self, serializer):
        # serializer.save()
        user = serializer.create(serializer.validated_data)
        user.set_password(serializer['password'])
        user.save()
