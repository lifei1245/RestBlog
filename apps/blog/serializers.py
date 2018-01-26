# coding=utf-8
# @Time : 2018/1/22 13:27
# @Author : 李飞
from django.forms import widgets
from rest_framework import serializers

from .models import Blog, Category, Comment
import datetime
from user.serializers import UserDetailSerializer


class CategorySerializer(serializers.ModelSerializer):
    import datetime
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.HiddenField(default=datetime.datetime.now())

    class Meta:
        model = Category
        fields = '__all__'


class BlogSimpleSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    author = UserDetailSerializer(many=False)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(many=False)
    category = CategorySerializer(many=False)

    class Meta:
        model = Blog
        fields = '__all__'


class CreateBlogSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, default=datetime.datetime.now())
    content = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'}, help_text='内容')

    class Meta:
        model = Blog
        fields = ('tittle', 'author', 'content', 'add_time', 'category')


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, default=datetime.datetime.now())

    class Meta:
        model = Comment
        fields = '__all__'


class MyCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    blog = BlogSimpleSerializer(many=False)

    class Meta:
        model = Comment
        fields = '__all__'
