# coding=utf-8
# @Time : 2018/1/22 17:35
# @Author : 李飞

import django_filters
from .models import Blog, Comment


class BlogFilter(django_filters.rest_framework.FilterSet):
    # tittle = django_filters.CharFilter(name='tittle', lookup_expr='contains', help_text='名称')
    # content = django_filters.CharFilter(name='content', lookup_expr='contains', help_text='名称')
    # author = django_filters.CharFilter(name='author', lookup_expr='contains', help_text='名称')

    class Meta:
        model = Blog
        fields = ['category']


class CommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Comment
        fields = ['blog']
