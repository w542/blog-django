from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


# 自定义feed_type来实现：
class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        # for i in item:
        #     print(i)
        # item['content_html'] 出问题， item是一个字典，拿不到key=content_html
        # handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = "myBlog ststem"
    link = '/rss/'
    description = 'myBlog is a blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post_detail', args=[item.pk])