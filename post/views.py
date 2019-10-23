from django.shortcuts import render

from .models import Post


def detail_view(request):
    pass


def list_view(request):
    return render(request, 'main/home.html', {'posts': Post.objects.all()})
