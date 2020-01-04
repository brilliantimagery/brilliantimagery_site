from datetime import datetime

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.fixture
def post_w_path_content(db):
    from post.models import Post, PostCategory

    content = '<p>Hello!!!</p> <p>Hello again.</p>'

    mixer.blend(User)
    category = mixer.blend(PostCategory,
                           category='Cat 1',
                           slug_category='cat1')
    post = mixer.blend(Post,
                       content=content,
                       slug_post='heres-a-slug',
                       category_id=1,
                       publish_date=datetime(2018, 8, 15))
    yield post, '/cat1/2018-08-15/heres-a-slug/', content
