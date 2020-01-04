import os

from django.contrib.auth.models import User
from django.test import TestCase
from mixer.backend.django import mixer
import pytest


def test_user_str(db_w_user):
    user = db_w_user
    profile = user.profile

    assert str(profile) == f'{user.username} Profile'


def test_user_save(db_w_updated_user):
    user, expected_username, expected_email = db_w_updated_user

    user.save()

    actual_user = User.objects.get(pk=1)

    assert actual_user.username == expected_username
    assert actual_user.email == expected_email


class TestProfileSave(TestCase):

    @pytest.mark.usefixtures('user_w_updated_image')
    def test_stuff(self):
        from django.db.models.fields.files import ImageFieldFile
        from django.db.models import FileField
        from PIL import Image

        path = os.path.join(os.path.abspath('.'), 'account', 'tests', 'test_image2.jpg')
        user = User.objects.get(pk=1)
        user.profile.image = ImageFieldFile(instance=None, field=FileField(), name=path)

        with self.settings(MEDIA_ROOT=os.path.join(os.path.abspath('.'), 'account', 'tests'),
                           MEDIA_URL='/tests'):
            user.profile.save()

        image = Image.open(path)
        assert image.width == 17
        assert image.height == 300
