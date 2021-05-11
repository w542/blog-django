from django.db import models
from blog.models import Post


# 评论
class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    target = models.CharField(max_length=100, verbose_name='评论目标')
    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 此处需要改进
    @classmethod
    def get_by_target(cls, target):
        # 此处的target 是 views.py 传过来的path
        qs = cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
        return qs

    class Meta:
        verbose_name = verbose_name_plural = '评论'

