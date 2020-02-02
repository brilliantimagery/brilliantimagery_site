"""bi_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views
# from .views import PostCreateView, PostDeleteView, PostDetailView, PostUpdateView, UserPostListView
from .views import PostCreateView, PostDeleteView, PostUpdateView

app_name = 'post-slugged'

urlpatterns = [
    path('', views.root_view, name='root-view'),
    path('<slug:date_slug>/<slug:post_slug>/', views.detail_view, name='detail-view'),
    path('<slug:date_slug>/<slug:post_slug>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<slug:date_slug>/<slug:post_slug>/update/', PostUpdateView.as_view(), name='update'),
    path('<slug:date_slug>/<slug:post_slug>/comment/', views.comment_view, name='comment'),
    path('<slug:date_slug>/<slug:post_slug>/update_comment/', views.update_comment_view, name='update_comment'),
]
