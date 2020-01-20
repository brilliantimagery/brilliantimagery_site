from django.shortcuts import render

from post.models import Post
from post.views import _sidebar


def about_view(request):
    context = {'sidebar': _sidebar()}

    return render(request, 'main/about.html', context=context)


def downloads_view(request):
    context = {'sidebar': _sidebar()}

    return render(request, 'main/downloads.html', context=context)


# def download_manager(request, file_name):
#     context = {'sidebar': _sidebar()}
#
#     return render(request, 'main/downloads.html', context=context)


def license_view(request):
    context = {'sidebar': _sidebar()}

    return render(request, 'main/license.html', context=context)
