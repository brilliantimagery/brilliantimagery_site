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

# from .views import PostCreateView, UserPostListView
from .views import PostCreateView, user_post_list_view

app_name = 'post'

urlpatterns = [
    path('new/', PostCreateView.as_view(), name='create-new'),
    # path('<slug:username>/', UserPostListView.as_view(), name='user-posts'),
    path('<slug:username>/', user_post_list_view, name='user-posts'),
]
