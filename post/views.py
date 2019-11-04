from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from .models import Post


def detail_view(request):
    pass


def series_view(request, slug_category, slug_series):
    posts = Post.objects.filter(series__slug_series=slug_series).order_by('-publish_date').all()
    return render(request, 'post/post_list.html', {'posts': posts})


def category_view(request, slug_category):
    posts = Post.objects.filter(series__category__slug_category=slug_category).order_by('-publish_date').all()
    return render(request, 'post/post_list.html', {'posts': posts})


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'series', 'slug_post']

    def form_valid(self, form):
        form.instance.author


class PostDetailView(DetailView):
    model = Post


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'  # get rid of this and change all 'post' references to 'object_list" refs
    ordering = ['-publish_date']

