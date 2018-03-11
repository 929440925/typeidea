# coding:utf-8
from __future__ import unicode_literals 

import re 
import xadmin 
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url, include 
from django.views.decorators.cache import cache_page
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from blog.views import IndexView, CategoryView, TagView, PostView, AuthorView
from blog.api import PostViewSet,CategoryViewSet,TagViewSet,UserViewSet 
from blog.feeds import AllPostRssFeed 
from config.views import LinkView  
from comment.views import CommentView 
from typeidea import adminx #NOQA
from .autocomplete import CategoryAutocomplete, TagAutocomplete 

router = routers.DefaultRouter()
router.register(r'post',PostViewSet)
router.register(r'category',CategoryViewSet)
router.register(r'tag',TagViewSet)
router.register(r'user',UserViewSet)

def static(prefix, **kwargs):
    return [
        url(r'^%s(?P<path>.*)$' %re.escape(prefix.lstrip('/')), serve, kwargs=kwargs)
    ]

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^feed/rss/$',AllPostRssFeed(),name="rss"),
    url(r'^category/(?P<category_id>\d+)/', cache_page(60 * 10)(CategoryView.as_view()), name="category"),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="tag"),
    url(r'^post/(?P<pk>\d+)/$', PostView.as_view(), name="detail"),
    url(r'^author/(?P<author_id>\d+)/$', AuthorView.as_view(), name="author"),
    url(r'^links/$',LinkView.as_view(), name="links"),
    url(r'^comment/$',CommentView.as_view(), name="comment"),
    url(r'^admin/', xadmin.site.urls),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name="category-autocomplete"),
    url(r'tag-autocomplete/$', TagAutocomplete.as_view(),name="tag-autocomplete"),
    url(r'ckeditor/',include('ckeditor_uploader.urls')),
    url(r'^markdownx/',include('markdownx.urls')),
    url(r'^api/docs/', include_docs_urls(title='typeidea apis')),
    url(r'^api/',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        #url(r'^silk/',include('silk.urls',namespace='silk')),
    ] + urlpatterns 
