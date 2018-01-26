# coding=utf-8
# @Time : 2018/1/19 18:07
# @Author : 李飞
import xadmin
from .models import Blog, Comment, Category


class BlogAdmin(object):
    list_display = ["tittle", "author", "content", 'click_num', 'fav_num', 'image', 'category']


class CommentAdmin(object):
    list_display = ['user', 'content', 'blog']


class CategoryAdmin(object):
    list_display = ['user', 'tittle', ]


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Category, CategoryAdmin)
