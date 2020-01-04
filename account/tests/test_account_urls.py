from django.urls import reverse, resolve


class TestAccountUrls:

    def test_privacy_policy_url(self):
        path = reverse('account:privacy_policy')
        assert resolve(path).view_name == 'account:privacy_policy'

    def test_profile_url(self):
        path = reverse('account:profile')
        assert resolve(path).view_name == 'account:profile'

    def test_register_url(self):
        path = reverse('account:register')
        assert resolve(path).view_name == 'account:register'
