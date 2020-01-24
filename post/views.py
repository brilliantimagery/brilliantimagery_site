# from datetime.datetime import strptime
import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Post, PostComment, PostCategory
from .forms import NewCommentForm

pagination_count = 4
posts_per_sidebar_topic = 5


def detail_view(request, slug_category, date_slug, slug_post):
    post = get_object_or_404(Post, slug_post=slug_post)

    context = {'post': post, 'sidebar': _sidebar()}
    return render(request, 'post/post_detail.html', context=context)


def home_view(request):
    posts = Post.objects.order_by('-publish_date').all()
    paginated_posts = Paginator(posts, pagination_count)
    page = request.GET.get('page')
    posts = paginated_posts.get_page(page)

    context = {'object_list': posts, 'sidebar': _sidebar()}
    return render(request, 'post/post_list.html', context=context)


def user_post_list_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-publish_date')
    paginated_posts = Paginator(posts, pagination_count)
    page = request.GET.get('page')
    posts = paginated_posts.get_page(page)

    context = {'object_list': posts, 'sidebar': _sidebar(author=user)}
    return render(request, 'post/post_list.html', context=context)


def comment_view(request, slug_category, date_slug, slug_post):
    post_id = int(request.GET.get('post-id', '0'))
    comment_id = int(request.GET.get('comment-id', '0'))

    post_comment = PostComment()
    if request.user.is_authenticated:
        user = request.user
        post_comment.author = user
        post_comment.name = user.username
        post_comment.email = request.user.email
    else:
        user = None
        post_comment.username = request.POST.get('username', '')
        post_comment.email = request.POST.get('email', '')

    if request.method == 'GET':
        form = NewCommentForm(instance=post_comment)
        form.post_id = post_id
        form.comment_id = comment_id if comment_id else None
    else:
        form = NewCommentForm(request.POST)

        if form.is_valid():
            post_comment = PostComment()
            post_comment.author = user
            post_comment.username = form.cleaned_data.get('username')
            post_comment.email = form.cleaned_data.get('email')
            post_comment.comment = form.cleaned_data.get('comment')
            post_comment.post_comment_id = post_id
            post_comment.comment_comment_id = comment_id if comment_id else None
            post_comment.save()
            post_comment.comment = None

            return redirect('post-slugged:detail-view',
                            slug_category=slug_category,
                            date_slug=date_slug,
                            slug_post=slug_post)
        else:
            post_comment.comment = request.POST.get('comment', '')

        form = NewCommentForm(instance=post_comment)

    # timezone stuff likely causing an issue
    post = get_object_or_404(Post,
                             # category__slug_category=slug_category,
                             # publish_date=datetime.datetime.strptime(date_slug, "%Y-%m-%d"),
                             slug_post=slug_post)

    context = {'post': post,
               'form': form,
               'button_name': 'Comment',
               'sidebar': _sidebar()
               }

    return render(request, 'post/post_detail.html', context=context)


# @permission_required
# @user_passes_test()
@login_required
def update_comment_view(request, slug_category, date_slug, slug_post):
    post_id = int(request.GET.get('post-id', '0'))
    comment_id = int(request.GET.get('comment-id', '0'))
    user = request.user

    comment = get_object_or_404(PostComment, post_comment_id=post_id, pk=comment_id)

    if comment.author != user and \
            not user.groups.filter(permissions__name__iexact='can change post comment').exists():
        raise PermissionDenied

    if request.method == 'GET':
        form = NewCommentForm(instance=comment)
        form.post_id = post_id
        form.comment_id = comment_id
    else:
        form = NewCommentForm(request.POST)

        if form.is_valid():
            comment.comment = form.cleaned_data.get('comment')
            comment.save()

            return redirect('post-slugged:detail-view',
                            slug_category=slug_category,
                            date_slug=date_slug,
                            slug_post=slug_post)
        else:
            comment.comment = request.POST.get('comment', '')

        form = NewCommentForm(instance=comment)

    post = get_object_or_404(Post, slug_post=slug_post)

    context = {'post': post,
               'form': form,
               'button_name': 'Update'
               }
    return render(request, 'post/post_detail.html', context=context)


def category_view(request, slug_category):
    posts = Post.objects.filter(category__slug_category=slug_category). \
        order_by('-publish_date').all()

    paginated_posts = Paginator(posts, pagination_count)
    page = request.GET.get('page')
    posts = paginated_posts.get_page(page)

    return render(request, 'post/post_list.html',
                  {'object_list': posts,
                   'sidebar': _sidebar(category__name__iexact=slug_category)})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'slug_post']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    slug_field = 'slug_post'
    slug_url_kwarg = 'slug_post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# class PostDetailView(DetailView, CreateView):
#     model = Post
#     fields = ['email', 'comment']
#
#     slug_field = 'slug_post'
#     slug_url_kwarg = 'slug_post'


# class PostListView(ListView):
#     model = Post
#     ordering = ['-publish_date']
#     pagination_count = 5


# class UserPostListView(ListView):
#     model = Post
#     pagination_count = 5
#
#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-publish_date')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'slug_post']

    slug_field = 'slug_post'
    slug_url_kwarg = 'slug_post'
    redirect_field_name = 'post:detail-view'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def _sidebar(**kwargs):
    # all_posts = Post.objects.order_by('-publish_date').values('title', 'category__slug_category', 'publish_date', 'slug_post')[:results_per_subset]

    filters = kwargs.copy()
    filters.pop('category__name', None)
    filters.pop('category__name__iexact', None)
    all_posts = Post.objects.filter(**filters).order_by('-publish_date')[:posts_per_sidebar_topic]
    sidebar = {'All Posts': all_posts}

    categories = PostCategory.objects.values_list('name', flat=True)

    for cat in categories:
        posts = Post.objects.filter(**kwargs).order_by('-publish_date'). \
                    filter(category__name__iexact=cat)[: posts_per_sidebar_topic]
        if posts:
            sidebar[cat] = posts

    return sidebar
