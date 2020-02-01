from itertools import chain

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from post.models import Post, PostCategory


# class StaticViewSitemap(Sitemap):
#
#     def items(self):
#         return ['main:about',
#                 'main:license',
#                 ]
#
#     def location(self, obj):
#         return reverse(obj)


class SluggedViewSiteMap(Sitemap):

    def items(self):
        posts = Post.objects.all()
        category = PostCategory.objects.all()
        return list(chain(posts, category))
