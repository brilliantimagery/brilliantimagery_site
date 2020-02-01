from django.contrib.sitemaps.views import sitemap
from django.test import RequestFactory
from django.urls import reverse

from post.tests.conftest import six_posts


def test_sitemap(six_posts):
    from main.sitemap import SluggedViewSiteMap

    path = reverse('sitemap')
    request = RequestFactory().get(path)

    sitemaps = {'slugged': SluggedViewSiteMap,
                }

    response = sitemap(request, sitemaps=sitemaps)

    assert response.status_code == 200
    assert '<loc>http://testserver/main/about/</loc>' in response.rendered_content
    assert '<loc>http://testserver/other/2018-04-15/slug-4/</loc>' in response.rendered_content
