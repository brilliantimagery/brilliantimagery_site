from unittest.mock import patch

from django.test import RequestFactory
from django.urls import reverse


def test_about_view():
    from main.views import about_view

    path = reverse('main:about')
    request = RequestFactory().get(path)

    with patch('main.views._sidebar', return_value={}):
        response = about_view(request)

    assert response.status_code == 200
    assert b'<h1>Brilliant Imagery</h1>' in response.content


def test_license_view():
    from main.views import license_view

    path = reverse('main:license')
    request = RequestFactory().get(path)

    with patch('main.views._sidebar', return_value={}):
        response = license_view(request)

    assert response.status_code == 200
    assert b'<h1>License</h1>' in response.content
