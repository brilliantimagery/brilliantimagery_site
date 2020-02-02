import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PostCategory(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    root_slug = models.CharField(max_length=200, default=1)
    comments_enabled = models.BooleanField(default=True)
    is_root_post = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'PostCategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post-slugged:root-view',
                       kwargs={'root_slug': self.root_slug})


class Post(models.Model):
    title: str = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    content: str = models.TextField()
    publish_date: datetime = models.DateTimeField(default=timezone.now, blank=True)
    category = models.ForeignKey(PostCategory, default=1, verbose_name='category',
                                 on_delete=models.SET_DEFAULT)
    post_slug = models.CharField(max_length=200, default='', unique=True, null=True, blank=True)
    comments_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} - {datetime.datetime.strftime(self.publish_date, "%Y-%m-%d")}'

    @property
    def content_summary(self):
        splitter = '</p>'
        if splitter in self.content:
            return self.content.split(splitter)[0] + splitter
        return self.content

    def get_absolute_url(self):
        if self.category.is_root_post:
            return reverse('post-slugged:root-view',
                           kwargs={'root_slug': self.post_slug}
                           )
        else:
            return reverse('post-slugged:detail-view',
                           kwargs={'root_slug': self.category.root_slug,
                                   'date_slug': self.publish_date.strftime('%Y-%m-%d'),
                                   'post_slug': self.post_slug}
                           )


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    name = models.CharField(max_length=50, default='', null=True, blank=True)
    email = models.CharField(max_length=50, default='', null=True, blank=True)
    publish_date: datetime = models.DateTimeField(default=timezone.now, blank=True)
    comment: str = models.TextField(default='')
    comments_enabled = models.BooleanField(default=True)

    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, default=1,
                                     related_name='post_comments', null=True, blank=True)
    comment_comment = models.ForeignKey('self', on_delete=models.CASCADE, default=None,
                                        related_name='comment_comments', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'PostComments'

    def __str__(self):
        return self.comment[:100]
