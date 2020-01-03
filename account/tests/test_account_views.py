import os

from django.contrib.auth.models import Group, User, AnonymousUser
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.http import QueryDict
from django.test import RequestFactory
import pytest
from django.urls import reverse
from django.utils.datastructures import MultiValueDict
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
def profile_request(factory):
    path = reverse('account:profile')
    yield factory.get(path)


@pytest.fixture
def profile_anonymous_user_get_request(profile_request):
    profile_request.method = "GET"
    profile_request.user = AnonymousUser()
    yield profile_request


@pytest.fixture
def profile_logged_in_get_request(profile_request, db):
    request = profile_request
    request.method = "GET"
    request.user = mixer.blend(User, username='user1', email='user1@address.com')
    yield request


@pytest.fixture
def profile_logged_in_post_request(profile_logged_in_get_request, db):
    request = profile_logged_in_get_request
    request.method = "POST"
    request.POST = QueryDict('username=user1&email=user1@address.com')
    # file = InMemoryUploadedFile
    path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image.jpg')
    with open(path, 'rb') as f:
        file = SimpleUploadedFile('test_image.jpg', f.read())
    request.FILES['image'] = [file]
    yield request


@pytest.fixture
def profile_logged_in_invalid_form_post_request(profile_logged_in_post_request, db):
    request = profile_logged_in_post_request
    request.POST = QueryDict('username=user1')
    yield request


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


def test_profile_not_logged_in(profile_anonymous_user_get_request):
    from account.views import profile

    response = profile(profile_anonymous_user_get_request)

    assert response.status_code == 302
    assert '/account/login/?next=/account/profile/' in response.url


def test_profile_logged_in_get(profile_logged_in_get_request, db):
    from account.views import profile

    response = profile(profile_logged_in_get_request)

    assert response.status_code == 200
    assert b'<input type="text" name="username" value="user1" maxlength="150" class="textinput ' \
           b'textInput form-control" required id="id_username">' in response.content
    assert b'Currently: <a href="/media/default.jpg">default.jpg</a>' in response.content


def test_profile_logged_in_post(profile_logged_in_post_request, db):
    from unittest.mock import patch
    from account.views import profile

    with patch('django.forms.forms.BaseForm.is_valid', return_value=True):
        with patch('django.forms.models.BaseModelForm.save', return_value=True):
            with patch('django.contrib.messages.success', return_value=None):
                response = profile(profile_logged_in_post_request)

    assert response.status_code == 302
    assert response.url == '/account/profile/'


def test_profile_logged_in_invalid_form_post(profile_logged_in_invalid_form_post_request, db):
    from account.views import profile

    response = profile(profile_logged_in_invalid_form_post_request)

    assert response.status_code == 200
    assert b'<input type="text" name="username" value="user1" maxlength="150" class="textinput ' \
           b'textInput form-control" required id="id_username">' in response.content
