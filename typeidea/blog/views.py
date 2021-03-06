# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
# from django.db import connection #引入数据库的列表
from django.core.cache import cache
from django.views.generic import ListView, DetailView
# from silk.profiling.profiler import silk_profile

from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment
from comment.views import CommentShowMixin
logger = logging.getLogger(__name__)


def cache_it(func):
    def wrapper(self, *args, **kwargs):
        key = repr((func.__name__, args, kwargs))
        result = cache.get(key)
        if result:
            return result
        result = func(self, *args, **kwargs)
        cache.set(key, result, 60 * 5)
        return result
    return wrapper


class CommonMixin(object):
    @cache_it
    def get_category_context(self):
        categories = Category.objects.filter(status=1)

        nav_cates=[]
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)
        return {
            'nav_cates': nav_cates,
            'cates': cates,
        }

    def get_context_data(self, **kwargs):
        side_bars = SideBar.objects.filter(status=1)

        recently_posts = Post.objects.filter(status=1)[:10]
        hot_posts = Post.objects.filter(status=1).order_by('-pv')[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]

        kwargs.update({
            'side_bars': side_bars,
            'recently_comments': recently_comments,
            'recently_posts': recently_posts,
            'hot_posts': hot_posts,
        })
        kwargs.update(self.get_category_context())
        return super(CommonMixin, self).get_context_data(**kwargs)


class BasePostsView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 5  # 分页


def time_it(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, 'cost', time.time() - start)
        return result
    return wrapper


class IndexView(BasePostsView):
    @time_it
    def get_queryset(self):
        query = self.request.GET.get('query')
        logger.info('query:[%s]', query)
        qs = super(IndexView, self).get_queryset()
        if query:
            qs= qs.filter(title__icontains=query)  # select * from blog_post where title ilike '%query%'
        logger.info('query result:[%s]', qs)
        return qs

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        return super(IndexView, self).get_context_data(query=query)


class CategoryView(BasePostsView):
    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cate_id)
        return qs


class TagView(BasePostsView):
    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return []
        posts = tag.posts.all()
        return posts


class AuthorView(BasePostsView):
    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        qs = super(AuthorView, self).get_queryset()
        author_id = self.request.GET.get('author_id')
        if author_id:
            qs = qs.filter(owner_id=author_id)
        return qs


class PostView(CommonMixin, CommentShowMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostView, self).get(request, *args, **kwargs)
        self.pv_uv()
        return response

    def pv_uv(self):
        # 添加pv
        # 判断用户， 添加uv
        # TODO:判断用户24小时内有没有访问
        sessionid = self.request.COOKIES.get('sessionid')
        path = self.request.path

        if not sessionid:
            return

        pv_key = 'pv:%s:%s' % (sessionid, path)
        # import pdb; pdb.set_trace()
        if not cache.get(pv_key):
            self.object.increse_pv()
            cache.set(pv_key, 1, 60)

        uv_key = 'uv:%s:%s' % (sessionid, path)
        if not cache.get(uv_key):
            self.object.increse_uv()
            cache.set(uv_key, 1, 60 * 60 *24)
