"""myBlog_Django_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps import views as sitemap_views

from .custom_site import custom_site
from config.views import LinkListView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import (IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag_list'),
    path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),

    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post_detail' ),
    path('links/', LinkListView.as_view(), name='links'),
    path('search/', SearchView.as_view(), name='search'),
    path('comment/', CommentView.as_view(), name='comment'),

    path('latest/rss/', LatestPostFeed(), name='rss'),
    path('sitemap.xml', sitemap_views.sitemap, {'sitemaps':{'posts': PostSitemap}}),

    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
]
