from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Post, PostCategory, PostSeries


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title/date', {'fields': ['title', 'publish_date', 'author']}),
        ('URL', {'fields': ['slug_post']}),
        ('Series', {'fields': ['series']}),
        ('Content', {'fields': ['content']}),
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(PostSeries)
