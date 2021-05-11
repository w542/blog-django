import mistune

from django.db import models
from django.contrib.auth.models import User
# 把返回的数据绑到实例上
from django.utils.functional import cached_property


# 分类
class Category(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    # 配置Model属性
    class Meta:
        verbose_name = verbose_name_plural = '分类'

    # 一次I/O
    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


# 标签
class Tag(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


# 文章
class Post(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')  # blank 填写表单可以为空，sql中存空字符串
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    content_html = models.TextField(verbose_name='正文MD的html形式', blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id'] # 根据id进行降序排序

    # 保存数据，大部分Django直接处理了
    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_tagName(id):
        """
        根据tag_id 查询出tag，和与之相关的post的list
        :param tag_id: 标签ID
        :return: post_list, tag
        """
        try:
            tag = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            # post_set 跟外键有关
            # post的model存在一个到tag的外键，自动为tag反向生成一个字段
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        """
         根据category_id 查询出category，和与之相关的post的list
        :param category_id: 分类ID
        :return: post_list, category
        """
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    # 为实现sitemap 输出 tags, 这个再议
    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))

