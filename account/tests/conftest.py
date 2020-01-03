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
def db_w_group(db):
    mixer.blend(Group, name='basic_web_user')
    yield None


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
def login_request_request(factory):
    path = reverse('account:login')
    yield factory.get(path)


@pytest.fixture
def login_get_request(login_request_request):
    request = login_request_request
    request.method = "GET"
    yield request


@pytest.fixture
def login_w_valid_db_user_post_request(login_request_request, db):
    request = login_request_request
    request.method = "POST"
    mixer.blend(User, username='user1', password='password1')
    request.POST = QueryDict('username=user1&password=password1')

    yield request


@pytest.fixture
def logout_request_request(factory):
    path = reverse('account:logout')
    yield factory.get(path)


@pytest.fixture
def privacy_policy_request(factory):
    path = reverse('account:privacy_policy')
    yield factory.get(path)


