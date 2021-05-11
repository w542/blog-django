from django.contrib import admin

from .models import Link, SideBar
from myBlog_Django_v1.base_admin import BaseOwnerAdmin
from myBlog_Django_v1.custom_site import custom_site

# Register your models here.


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):

    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    # 基类完成
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):

    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    # 基类完成
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(SideBarAdmin, self).save_model(request, obj, form, change)