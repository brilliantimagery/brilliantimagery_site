import datetime
import enum

from django.db import models
from django.utils import timezone


class KindEnum(models.Field):
    def __init__(self, *args, **kwargs):
        super(KindEnum, self).__init__(*args, **kwargs)
        if not self.choices:
            raise AttributeError('EnumField requires `choices` attribute.')

    def db_type(self):
        return "enum(%s)" % ','.join("'%s'" % k for (k, _) in self.choices)

    DNG101 = 'd'
    POST = 'p'
    TUTORIAL = 't'
    KIND_CHOICES = (
        (DNG101, 'DNG101'),
        (POST, 'POST'),
        (TUTORIAL, 'TUTORIAL'),
    )


class Post(models.Model):
    title: str = models.CharField(max_length=200)
    content: str = models.TextField()
    publish_date: datetime = models.DateTimeField(default=timezone.now, blank=True)
    kind: enum.Enum = models.CharField(max_length=1, choices=KindEnum.KIND_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {datetime.datetime.strftime(self.publish_date, "%Y-%m-%d")}'
