from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from myBlog_Django_v1.custom_site import custom_site
from myBlog_Django_v1.base_admin import BaseOwnerAdmin

# Register your models here.


# 在同一页面编辑关联数据
class PostInline(admin.TabularInline):  # StackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1   # 控制额外多几个
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只展示当前用户分类
    """

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        # 根据用户筛选分类
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        # 根据网页参数 筛选 lookups 返回的queryset
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# site 将Category这个model分到另一站点
@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('owner', 'name', 'status', 'is_nav', 'created_time', 'post_count')    # 保存后显示列表
    fields = ('name', 'status', 'is_nav')   # 控制页面上要显示的字段
    # list_filter = [CategoryOwnerFilter]
    # inline admin
    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # Form 实现
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator', 'owner'
    ]
    list_display_links = [] # 配置哪些字段可以作为链接
    list_filter = ['category', ]  # 配置页面过滤器
    search_fields = ['title', 'category_name']  # 配置搜索字段
    actions_on_top = True   # 是否展示在顶部
    actions_on_bottom = True    # 是否展示在底部
    save_on_top = True  # 保存、编辑、编辑并新建的按钮是否在顶部
    # 编辑页面
    fieldsets = (
        ('基础配置',{
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    # 自定义函数
    # 需要加强
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=[obj.id])
        )

    operator.short_description = '操作'
    # 暂时不用
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = {
    #         'https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',
    #     }


@admin.register(LogEntry )
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id',
                    'action_flag', 'user',
                    'change_message']
