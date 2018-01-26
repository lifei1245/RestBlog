from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from blog.permissions import IsOwnerOrReadOnly
from .models import FavBlog
from .serializers import FavBlogSerializer, FavBlogListSerializer
from blog.models import Blog


# Create your views here.


class FavBlogViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    """
    create:
        用户新建收藏
    list:
        获取用户收藏列表
    destroy:
        删除收藏
    """
    queryset = FavBlog.objects.all()
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'list':
            return FavBlogListSerializer
        else:
            return FavBlogSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fav_blog = FavBlog.objects.filter(user=self.request.user, blog_id=serializer.initial_data['blog'])
        if fav_blog:
            headers = self.get_success_headers(serializer.data)
            return Response({'msg': '已经收藏'}, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            blog = Blog.objects.filter(id=serializer.initial_data['blog'])[0]
            blog.fav_num += 1
            blog.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        header = self.get_success_headers({'msg': '取消收藏成功'})
        return Response({'msg': '取消收藏成功'}, status=status.HTTP_204_NO_CONTENT, headers=header)
