from django.shortcuts import render

from .models import Post


def detail_view(request):
    pass


def series_view(request, slug_category, slug_series):
    posts = Post.objects.filter(series__slug=slug_series).order_by('-publish_date').all()
    return render(request, 'post/post_list.html', {'posts': posts})


def category_view(request, slug_category):
    posts = Post.objects.filter(series__category__slug=slug_category).order_by('-publish_date').all()
    return render(request, 'post/post_list.html', {'posts': posts})
