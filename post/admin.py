from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Post, PostComment, PostCategory


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title/date', {'fields': ['title', 'publish_date', 'author']}),
        ('URL', {'fields': ['slug_post']}),
        ('Category', {'fields': ['category']}),
        ('Content', {'fields': ['content', 'comments_enabled']}),
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(PostComment)

