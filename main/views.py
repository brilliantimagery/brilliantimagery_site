from django.shortcuts import render
from django.views.generic import ListView

from post.models import Post


def home(request):
    return render(request, 'post/post_list.html', {'posts': Post.objects.order_by('-publish_date').all()})


# class PostListView(ListView):
#     model = Post
#     context_object_name = 'posts' # get rid of this and change all 'post' references to 'object_list" refs
#     ordering = ['-publish_date']
