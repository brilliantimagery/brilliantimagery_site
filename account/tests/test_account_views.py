from django.contrib.auth.models import Group, User
from django.http import QueryDict
from django.test import RequestFactory
import pytest
from django.urls import reverse
from mixer.backend.django import mixer


@pytest.fixture(scope='module')
def factory():
    yield RequestFactory()


@pytest.fixture
def register_request(factory):
    path = reverse('account:register')
    yield factory.get(path)


@pytest.fixture
def register_get_request(register_request):
    register_request.method = "GET"
    yield register_request


@pytest.fixture
def register_post_request(register_request):
    register_request.method = "POST"
    yield register_request


@pytest.fixture
def register_valid_post_request(register_post_request):
    register_post_request.POST = QueryDict('username=user1&email=user1@address.com&'
                                           'password1=lkjytrfds&password2=lkjytrfds')
    yield register_post_request


@pytest.fixture
def register_password_mismatch_post_request(register_post_request):
    register_post_request.POST = QueryDict('username=user1&email=user1@address.com&'
                                           'password1=lkjytrfds&password2=lktrfds')
    yield register_post_request


@pytest.fixture
def db_w_group(db):
    mixer.blend(Group, name='basic_web_user')
    yield None


def test_register_get(register_get_request, db):
    from account.views import register

    response = register(register_get_request)
    expected_username_field = b'<input type="text" name="username" maxlength="150" autofocus class="textinput ' \
                              b'textInput form-control" required id="id_username">'

    assert response.status_code == 200
    assert b'Join Today' in response.content
    assert expected_username_field in response.content


def test_register_post_valid(register_valid_post_request, db_w_group):
    from account.views import register

    from unittest.mock import patch
    with patch('django.contrib.messages.success', return_value=None):
        with patch('django.contrib.auth.login', return_value=None):
            with patch('django.contrib.messages.info', return_value=None):
                response = register(register_valid_post_request)
    assert response.status_code == 302
    assert response.url == '/'


# def test_register_post_user_exists(register_valid_post_request, db_w_group):
#     from account.views import register
#
#     from unittest.mock import patch
#     with patch('django.contrib.messages.success', return_value=None):
#         with patch('django.contrib.auth.login', return_value=None):
#             with patch('django.contrib.messages.info', return_value=None):
#                 response = register(register_valid_post_request)
#     assert response.status_code == 302
#     assert response.url == '/'


def test_register_post_password_mismatch(register_password_mismatch_post_request, db_w_group):
    from account.views import register

    from unittest.mock import patch
    with patch('django.contrib.messages.error', return_value=None):
        response = register(register_password_mismatch_post_request)
    assert response.status_code == 200
    assert b'<input type="text" name="username" value="user1" maxlength="150" autofocus ' \
           b'class="textinput textInput form-control" required id="id_username">' in response.content


def test_profile_not_logged_in(factory, db):
    from django.contrib.auth.models import AnonymousUser
    from django.urls import reverse
    from account.views import profile

    path = reverse('account:profile')
    request = factory.get(path)
    request.user = AnonymousUser()

    response = profile(request)

    assert response.status_code == 302
    assert '/account/login/?next=/account/profile/' in response.url
