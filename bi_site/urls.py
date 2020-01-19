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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from post.views import home_view
from main.sitemap import StaticViewSitemap, SluggedViewSiteMap


sitemaps = {'static': StaticViewSitemap,
            'slugged': SluggedViewSiteMap,
            }

urlpatterns = [
    path('', home_view, name='home'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('docs/', include('docs.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('main/', include('main.urls')),
    path('posts/', include('post.urls')),
    path('<slug:slug_category>/', include('post.urls_slugged')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# categories = PostCategory.objects.values_list('category', flat=True).all()
# urlpatterns += [path(f'{c}/', include('post.urls')) for c in categories]

