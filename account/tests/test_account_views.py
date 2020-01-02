import pytest
from django.test import RequestFactory


@pytest.fixture
def factory():
    return RequestFactory()


def test_register_get(factory, db):
    from django.urls import reverse
    from account.views import register

    path = reverse('account:register')
    request = factory.get(path)
    request.method = 'GET'

    response = register(request)
    expected_username_field = b'<input type="text" name="username" maxlength="150" autofocus class="textinput ' \
                              b'textInput form-control" required id="id_username">'
    assert response.status_code == 200
    assert b'Join Today' in response.content
    assert expected_username_field in response.content

# def test_register_view(self):
#     from django.urls import reverse
#     from django.tests import RequestFactory
#     from account.views import register
#     post = QueryDict
#     # from mixer.backend.django import mixer
#     # from django.contrib.auth.models import User
#
#     from django.http import QueryDict
#     path = reverse('account:register')
#     request = RequestFactory().get(path)
#     # request.user = mixer.blend(User)
#     request.method = "POST"
#
#     response = register(request)
#     assert response.status_code == 200

def test_profile_not_logged_in(factory, db):
    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory
    from django.urls import reverse
    from account.views import profile

    path = reverse('account:profile')
    request = factory.get(path)
    request.user = AnonymousUser()

    response = profile(request)

    assert response.status_code == 302
    assert '/account/login/?next=/account/profile/' in response.url
