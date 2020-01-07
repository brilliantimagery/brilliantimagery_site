from copy import deepcopy
from datetime import datetime

import pytest
from django.contrib.auth.models import AnonymousUser, Group, Permission, User
from django.http import QueryDict
from django.urls import reverse
from mixer.backend.django import mixer

from account.tests.conftest import factory


@pytest.fixture
def post_w_path_content(db):
    from post.models import Post, PostCategory

    content = '<p>Hello!!!</p> <p>Hello again.</p>'

    mixer.blend(User)
    mixer.blend(PostCategory, category='Cat 1', slug_category='cat1')
    post = mixer.blend(Post,
                       content=content,
                       slug_post='heres-a-slug',
                       category_id=1,
                       publish_date=datetime(2018, 8, 15))

    yield post, '/cat1/2018-08-15/heres-a-slug/', content


@pytest.fixture
def five_posts(db):
    from post.models import Post, PostCategory, PostComment

    permission = mixer.blend(Permission,
                             codename='can_change_post_comment',
                             name='can change post comment')
    group = mixer.blend(Group, name='editor')
    group.permissions.add(permission)

    users = [mixer.blend(User, username='user1', email='user1@address.com'),
             mixer.blend(User, username='user2', email='user2@address.com'),
             mixer.blend(User, username='user3', email='user3@address.com')]

    group.user_set.add(users[1])
    group.save()

    categories = [mixer.blend(PostCategory, name='DNG101', slug_category='dng101'),
                  mixer.blend(PostCategory, name='other', slug_category='other')]

    posts = [mixer.blend(Post,
                         title=f'Title {i}',
                         content=f'Content {i}',
                         slug_post=f'slug-{i}',
                         category_id=1,
                         user_id=1,
                         publish_date=datetime(2018, i, 15))
             for i in range(1, 6)]

    posts[1].author_id = 2
    posts[3].author_id = 2
    posts[3].category_id = 2
    posts[4].category_id = 2
    [p.save() for p in posts]

    comments = [mixer.blend(PostComment,
                            author_id=None,
                            username='Anonymous',
                            email='anonymous@address.com',
                            comment="Here's a first comment",
                            post_comment_id=1,
                            comment_comment_id=None),
                mixer.blend(PostComment,
                            author_id=1,
                            username='user1',
                            email='user1@address.com',
                            comment="Here's a comment on the first comment",
                            post_comment_id=1,
                            comment_comment_id=1),
                ]

    yield posts, users, categories, comments


@pytest.fixture
def detail_view_request(factory):
    path = reverse('post-slugged:detail-view',
                   kwargs={'slug_category': 'hello',
                           'date_slug': 'hello2',
                           'slug_post': 'hello3'}
                   )
    yield factory.get(path)


@pytest.fixture
def home_view_request(factory):
    path = reverse('home')
    yield factory.get(path)


@pytest.fixture
def home_view_request_page_2(home_view_request):
    request = home_view_request
    request.GET = QueryDict('page=2')
    yield request


@pytest.fixture
def user_post_list_request(factory):
    path = reverse('post:user-posts', kwargs={'username': 'user1'})
    yield factory.get(path)


@pytest.fixture
def user_post_list_request_page_2(user_post_list_request):
    request = user_post_list_request
    request.GET = QueryDict('page=2')
    yield request


@pytest.fixture
def comment_view_request(factory):
    path = reverse('post-slugged:comment', kwargs={'slug_category': 'dng101',
                                                   'date_slug': '2018-01-15',
                                                   'slug_post': 'slug-1'})
    yield factory.get(path)


@pytest.fixture
def comment_view_user_get_request(comment_view_request, five_posts):
    request = comment_view_request
    _, users, __, ___ = five_posts
    request.user = users[0]
    request.method = 'GET'
    yield request


@pytest.fixture
def comment_view_anonymous_get_request(comment_view_request):
    request = comment_view_request
    request.user = AnonymousUser()
    request.method = 'GET'
    yield request


@pytest.fixture
def comment_view_user_post_request(comment_view_request, five_posts):
    request = comment_view_request
    _, users, __, ___ = five_posts
    request.user = users[0]
    request.method = 'POST'
    request.GET = QueryDict('post-id=1&comment-id=0')
    request.POST = QueryDict('username=user1&email=user1@address.com&comment=Here\'s a comment!')
    yield request


@pytest.fixture
def comment_view_anonymous_post_request(comment_view_request):
    request = comment_view_request
    request.user = AnonymousUser()
    request.method = 'POST'
    request.GET = QueryDict('post-id=1&comment-id=0')
    request.POST = QueryDict('username=user1&email=user1@address.com&comment=Here\'s a comment!')
    yield request


@pytest.fixture
def update_comment_request(factory):
    path = reverse('post-slugged:update_comment', kwargs={'slug_category': 'dng101',
                                                          'date_slug': '2018-03-15',
                                                          'slug_post': 'slug-1'})
    yield factory.get(path)


@pytest.fixture
def update_comment_not_logged_in_get_request(update_comment_request):
    request = update_comment_request

    request.method = 'GET'
    request.user = AnonymousUser()
    request.GET = QueryDict('post-id=1&comment-id=2')

    yield request


@pytest.fixture
def update_comment_wrong_user_get_request(update_comment_not_logged_in_get_request, five_posts):
    request = update_comment_not_logged_in_get_request
    _, users, __, ___ = five_posts
    request.user = users[2]
    yield request


@pytest.fixture
def update_comment_author_get_request(update_comment_not_logged_in_get_request, five_posts):
    request = update_comment_not_logged_in_get_request
    _, users, __, ___ = five_posts
    request.user = users[0]
    yield request


@pytest.fixture
def update_comment_editor_get_request(update_comment_not_logged_in_get_request, five_posts):
    request = update_comment_not_logged_in_get_request
    _, users, __, ___ = five_posts
    request.user = users[1]
    yield request


@pytest.fixture
def update_comment_invalid_comment_post_request(update_comment_not_logged_in_get_request,
                                                five_posts):
    request = update_comment_not_logged_in_get_request
    _, users, __, ___ = five_posts
    request.user = users[0]
    request.method = 'POST'
    request.POST = QueryDict('comment=It failed, hard.&post-id=1&comment-id=2')
    yield request


@pytest.fixture
def update_comment_post_request(update_comment_invalid_comment_post_request, five_posts):
    request = update_comment_invalid_comment_post_request
    request.POST = QueryDict('comment=Here\'s an updated comment!!&post-id=1&comment-id=2')
    yield request
