from django.contrib import admin

from .models import Comment
from myBlog_Django_v1.custom_site import custom_site

# Register your models here.


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'created_time')
    # fields = ('target',)  # 没有fields 默认显示list_display