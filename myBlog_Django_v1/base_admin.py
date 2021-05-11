from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章、分类、标签、侧边栏、友链这些 Model 的 owner 字段
    2.用来针对 queryset 过滤当前用户的数据
    """
    exclude = ('owner', )

    # 重写 get_queryset() 对显示的数据集 做处理
    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    # 重写 save_model() 对于用户提交的数据进行补充，有些数据的权限不能给用户
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)