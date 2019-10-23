from django.shortcuts import render

from post.models import Post


def home(request):
    return render(request, 'main/home.html', {'posts': Post.objects.all()})
