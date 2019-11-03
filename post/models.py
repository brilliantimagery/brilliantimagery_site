import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PostCategory(models.Model):
    category = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, default=1)

    class Meta:
        verbose_name_plural = 'PostCategories'

    def __str__(self):
        return self.category


class PostSeries(models.Model):
    series = models.CharField(max_length=200)
    category = models.ForeignKey(PostCategory, default=1, verbose_name='category', on_delete=models.SET_DEFAULT)
    summary = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, default='')

    class Meta:
        verbose_name_plural = 'PostSeries'

    def __str__(self):
        return self.series


class Post(models.Model):
    title: str = models.CharField(max_length=200)
    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    content: str = models.TextField()
    publish_date: datetime = models.DateTimeField(default=timezone.now, blank=True)
    series = models.ForeignKey(PostSeries, default=1, verbose_name='series', on_delete=models.SET_DEFAULT)
    slug = models.CharField(max_length=200, default='')

    def __str__(self):
        return f'{self.title} - {datetime.datetime.strftime(self.publish_date, "%Y-%m-%d")}'

    @property
    def content_summary(self):
        splitter = '</p>'
        if splitter in self.content:
            return self.content.split(splitter)[0] + splitter
        return self.content
