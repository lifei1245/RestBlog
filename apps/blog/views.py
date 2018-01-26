from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from blog.filters import BlogFilter, CommentFilter
from blog.models import Blog, Category, Comment
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import BlogSerializer, BlogSimpleSerializer, CreateBlogSerializer, CategorySerializer, \
    CommentsSerializer, MyCommentSerializer
from rest_framework import filters


class BlogListSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 1000


class IntroduceBlogViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    list:
        推荐博客列表
    retrieve:
        推荐博客详情
    """
    pagination_class = BlogListSetPagination
    permission_classes = ()

    def get_queryset(self):
        return Blog.objects.filter(isintroduce=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogSimpleSerializer
        else:
            return BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    list:
        我的博客列表 \n
        参数:分页(page,pagesize),\n
        排序(ordering = [click_num,fav_num,add_time]),\n
        过滤(keyword,category［必须要是当前用户的类别，否则没有数据］)
    retrieve:
        博客详情
    create:
        新建博客
    """
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = BlogListSetPagination
    search_fields = ('tittle', 'content',)
    ordering_fields = ('click_num', 'fav_num', 'add_time')
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BlogFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)
        if self.action == 'list':
            filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogSimpleSerializer
        elif self.action == 'create':
            return CreateBlogSerializer
        else:
            return BlogSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            category = Category.objects.filter(id=category, user=self.request.user)
            if category:
                return Blog.objects.filter(author=self.request.user, category_id=category)
        return Blog.objects.filter(author=self.request.user)


class CategoryViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    list:
        获取用户的博客分类
    create:
        用户创建博客分类
    """
    serializer_class = CategorySerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(user=self.request.user)
        else:
            return Category.objects.all()


class CommentViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CommentsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CommentFilter
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        blog = self.request.query_params.get('blog', None)
        queryset = Comment.objects.filter(blog_id=blog)
        return queryset

    def list(self, request, *args, **kwargs):
        blog = request.query_params.get('blog', None)
        if blog:
            b = Blog.objects.filter(id=blog)
            if b:
                queryset = self.filter_queryset(self.get_queryset())

                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'msg': '数据错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': '请传入博客id'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        blog = request.data['blog']
        if blog:
            b = Blog.objects.filter(id=blog)
            if b:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({'msg': '数据错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': '请传入博客id'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(id=self.kwargs.get('pk'), user=self.request.user)
        obj = get_object_or_404(queryset, )
        self.check_object_permissions(self.request, obj)
        instance = obj
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyCommentViewSet(GenericViewSet, mixins.ListModelMixin):
    """
    list:
        我评论的列表
    """
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = MyCommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
