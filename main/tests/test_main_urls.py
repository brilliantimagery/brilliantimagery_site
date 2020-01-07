from django.urls import reverse, resolve


class TestMainUrls:

    def test_home_view_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'
