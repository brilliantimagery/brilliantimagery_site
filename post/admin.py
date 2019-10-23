from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Post


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title/date', {'fields': ['title', 'publish_date']}),
        ('Content', {'fields': ['content']}),
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Post, PostAdmin)
