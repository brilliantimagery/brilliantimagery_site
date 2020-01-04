import os

from django.contrib.auth.models import AnonymousUser, Group, Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
import pytest


@pytest.fixture
def user_w_updated_image(db_w_user):
    from shutil import copyfile

    user = db_w_user
    image_path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image.jpg')
    new_path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image2.jpg')

    copyfile(image_path, new_path)

    yield user, new_path

    os.remove(new_path)


@pytest.fixture(scope='module')
def factory():
    yield RequestFactory()


@pytest.fixture
def db_w_user(db):
    return mixer.blend(User, username='user1', email='user1@address.com')


@pytest.fixture
def db_w_updated_user(db_w_user):
    new_username = 'user1a'
    new_email = 'user1a@address.com'
    user = db_w_user
    user.username = new_username
    user.email = new_email
    return user, new_username, new_email


@pytest.fixture
def db_w_group(db):
    permission = mixer.blend(Permission, codename='do_stuff', name='Do Stuff')
    group = mixer.blend(Group, name='basic_web_user')
    group.permissions.add(permission)
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
