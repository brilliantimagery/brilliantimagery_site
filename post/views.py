from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Post


def series_view(request, slug_category, slug_series):
    posts = Post.objects.filter(series__slug_series=slug_series).order_by('-publish_date').all()
    return render(request, 'post/post_list.html', {'posts': posts})


def category_view(request, slug_category):
    posts = Post.objects.filter(series__category__slug_category=slug_category).order_by('-publish_date').all()
    return render(request, 'post/post_list.html', {'posts': posts})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'series', 'slug_post']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'series', 'slug_post']

    slug_field = 'slug_post'
    slug_url_kwarg = 'slug_post'
    redirect_field_name = 'post:detail-view'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    slug_field = 'slug_post'
    slug_url_kwarg = 'slug_post'


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'  # get rid of this and change all 'post' references to 'object_list" refs
    ordering = ['-publish_date']

