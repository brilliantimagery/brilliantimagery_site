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
from .views import PostCreateView, PostDetailView

app_name = 'post'

urlpatterns = [
    path('', views.category_view, name='category-view'),
    path('new/', PostCreateView.as_view(), name='create_view'),
    path('<slug_series>/', views.series_view, name='series_view'),
    path('<slug_series>/<slug_post>/', PostDetailView.as_view(), name='detail_view'),
]
