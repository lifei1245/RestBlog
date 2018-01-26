"""RestBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from RestBlog.settings import MEDIA_ROOT
from operations.views import FavBlogViewSet
from user.views import UserView, SmsSendViewSet, ChangePassWord
from blog.views import BlogViewSet, IntroduceBlogViewSet, CategoryViewSet, CommentViewSet, MyCommentViewSet
import xadmin

router = DefaultRouter()
router.register('sendsms', SmsSendViewSet, 'sendsms')
router.register('user', UserView, 'user')
router.register('blog', BlogViewSet, 'blog')
router.register('changepassword', ChangePassWord, 'changepassword')
router.register('introduceblog', IntroduceBlogViewSet, 'introduceblog')
router.register('category', CategoryViewSet, 'category')
router.register('favblog', FavBlogViewSet, 'favblog')
router.register('comment', CommentViewSet, 'comment')
router.register('mycomment', MyCommentViewSet, 'mycomment')

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r"docs/", include_docs_urls(title='博客api', public=False), ),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', obtain_jwt_token),
]
