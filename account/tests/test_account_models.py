import os

from mixer.backend.django import mixer
import pytest

from django.contrib.auth.models import User


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


# @pytest.fixture
# def user_w_updated_image(db_w_user, tmpdir):
#     from shutil import copyfile
#     from django.db.models import FileField
#     from django.db.models.fields.files import ImageFieldFile
#     from django.conf import settings
#
#     user = db_w_user
#     image_path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image.jpg')
#     new_path = os.path.join(tmpdir, 'test_image.jpg')
#
#     copyfile(image_path, os.path.join(tmpdir, new_path))
#
#     image = ImageFieldFile(instance=None, field=FileField(), name=image_path)
#     user.profile.image = image
#     root = tmpdir
#     url = os.path.split(tmpdir)[1]
#     yield user, new_path, root, url
#
#     os.remove(new_path)

@pytest.fixture
def user_w_updated_image(db_w_user):
    from shutil import copyfile

    user = db_w_user
    image_path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image.jpg')
    new_path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image2.jpg')

    copyfile(image_path, new_path)

    yield user, new_path

    os.remove(new_path)


def test_user_save(db_w_updated_user):
    user, expected_username, expected_email = db_w_updated_user

    user.save()

    actual_user = User.objects.get(pk=1)

    assert actual_user.username == expected_username
    assert actual_user.email == expected_email


from django.test import TestCase


class TestProfileSave(TestCase):

    @pytest.mark.usefixtures('user_w_updated_image')
    def test_stuff(self):
        path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image2.jpg')
        user = User.objects.get(pk=1)
        from django.db.models.fields.files import ImageFieldFile
        from django.db.models import FileField
        user.profile.image = ImageFieldFile(instance=None, field=FileField(), name=path)
        with self.settings(MEDIA_ROOT=os.path.join(os.path.abspath('.'), 'account', 'tests'),
                           MEDIA_URL='/tests'):
            user.profile.save()
        from PIL import Image
        image = Image.open(path)
        assert image.width == 17
        assert image.height == 300

# def test_profile_save(user_w_updated_image, tmp_path):
#     from django.conf import settings
#     user, image_path, MEDIA_ROOT, MEDIA_URL = user_w_updated_image
#     settings.MEDIA_ROOT = MEDIA_ROOT
#     settings.MEDIA_URL = MEDIA_URL
#     user.profile.save()
#     from PIL import Image
#     image = Image.open(image_path)
#     assert False
