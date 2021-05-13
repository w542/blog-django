from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from django.core.cache import cache

from .models import Post, Tag, Category
from config.models import SideBar


# Create your views here.
# render(request, template_name, context, content_type, status)
# 基于函数的视图，已经被基于类的视图所代替
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, tag = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {'post_list': post_list,
#                'tag': tag,
#                'category': category,
#                'sidebars': SideBar.get_all(),
#                }
#     context.update(Category.get_navs())
#
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {'post': post,
#                'sidebars': SideBar.get_all(),
#                }
#
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)


class CommonViewMinin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'sidebars': SideBar.get_all(),  # type(SideBar.get_all()) --> queryset
            }
        )
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMinin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'   # 模版中的变量名
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """
        继承了IndexView，所以对首页的qs过滤
        变成了对category_id过滤的文章
        重写queryset,根据分类过滤
        :return:
        """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')    # 从url参数中获取
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        # 前面的tag_id 去数据查询的？
        queryset = queryset.filter(tag=tag_id)
        return queryset


# 作者页：根据作者ID，得到关于该作者的文章列表
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')
        queryset = queryset.filter(owner_id=author_id)
        return queryset


class PostDetailView(CommonViewMinin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # 重写get()，用于实现访问量的统计--->重新设计，增加用户验证
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)
        self.handle_visited()
        return response

        # 调试用
        # from django.db import connection
        # print(connection.queries)
        # return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' %(uid, self.request.path)
        uv_key = 'pv:%s:%s:%s' %(uid, str(date.today), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('uv') + 1)
    # 已经用 组件 方式完成
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     path = self.request.path
    #     context.update({
    #         'comment_form': CommentForm,
    #         # self.request.path debug 看看内容是啥
    #         'comment_list': Comment.get_by_target(path)
    #     })
    #     return context


class SearchView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        else:
            # Q(title__icontains=) 实现了 （select * from post where title ilike ''）的sql语句
            return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword)
                                   | Q(tag__name__icontains=keyword) | Q(category__name__icontains=keyword))

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context


