# coding=utf-8
# @Time : 2018/1/25 13:30
# @Author : 李飞
from rest_framework import serializers
from .models import FavBlog
from blog.serializers import BlogSimpleSerializer


class FavBlogSerializer(serializers.ModelSerializer):
    import datetime
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.HiddenField(default=datetime.datetime.now())

    class Meta:
        model = FavBlog
        fields = '__all__'


class FavBlogListSerializer(serializers.ModelSerializer):
    import datetime
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.HiddenField(default=datetime.datetime.now())
    blog = BlogSimpleSerializer(many=False)

    class Meta:
        model = FavBlog
        fields = '__all__'
