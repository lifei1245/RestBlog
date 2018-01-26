# coding=utf-8
# @Time : 2018/1/19 13:39
# @Author : 李飞
from .models import UserProfile
import xadmin


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "api博客后台"
    site_footer = "blog"
    # menu_style = "accordion"


# class UserAdmin(object):
#     list_display = ['name', 'mobile', "email",'add']
#
#
# xadmin.site.register(UserProfile, UserAdmin)
