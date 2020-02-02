from unittest.mock import patch

import pytest
from django.core.exceptions import PermissionDenied


def test_detail_view(detail_view_request, post_w_path_content):
    from post.views import detail_view

    post, path, content = post_w_path_content

    with patch('post.views.get_object_or_404', return_value=post):
        response = detail_view(detail_view_request, root_slug='-', date_slug='-', post_slug='-')

    assert response.status_code == 200
    assert b'<p>Hello again.</p>' in response.content


def test_root_view(detail_main_and_date_request, post_w_path_content):
    from post.views import root_view

    post, path, content = post_w_path_content

    with patch('django.db.models.query.QuerySet.first', return_value=post):
        response = root_view(detail_main_and_date_request, root_slug='-')

    assert response.status_code == 200
    assert b'<p>Hello again.</p>' in response.content


def test_home_view_page_1(home_view_request, six_posts):
    from post.views import home_view

    with patch('post.views.pagination_count', 2):
        response = home_view(home_view_request)

    assert response.status_code == 200
    assert b'Content 1' not in response.content
    assert b'Content 2' not in response.content
    assert b'Content 3' not in response.content
    assert b'Content 4' in response.content
    assert b'Content 5' in response.content
    assert b'Content 6' not in response.content
    assert b'Title 1' in response.content
    assert b'Title 2' in response.content
    assert b'Title 3' in response.content
    assert b'Title 4' in response.content
    assert b'Title 6' not in response.content


def test_home_view_page_2(home_view_request_page_2, six_posts):
    from post.views import home_view

    with patch('post.views.pagination_count', 2):
        response = home_view(home_view_request_page_2)

    assert response.status_code == 200
    assert b'Content 1' not in response.content
    assert b'Content 2' in response.content
    assert b'Content 3' in response.content
    assert b'Content 4' not in response.content
    assert b'Content 5' not in response.content
    assert b'Content 6' not in response.content
    assert b'Title 1' in response.content
    assert b'Title 2' in response.content
    assert b'Title 3' in response.content
    assert b'Title 4' in response.content
    assert b'Title 5' in response.content
    assert b'Title 6' not in response.content


def test_user_post_list_page_1(home_view_request, six_posts):
    from post.views import user_post_list_view

    with patch('post.views.pagination_count', 2):
        response = user_post_list_view(home_view_request, 'user1')

    assert response.status_code == 200
    assert b'Content 1' not in response.content
    assert b'Content 2' not in response.content
    assert b'Content 3' not in response.content
    assert b'Content 4' not in response.content
    assert b'Content 5' in response.content
    assert b'Content 6' in response.content
    assert b'Title 1' in response.content
    assert b'Title 2' not in response.content
    assert b'Title 3' in response.content
    assert b'Title 4' not in response.content
    assert b'Title 5' in response.content
    assert b'Title 6' in response.content


def test_user_post_list_page_2(home_view_request_page_2, six_posts):
    from post.views import user_post_list_view

    with patch('post.views.pagination_count', 2):
        response = user_post_list_view(home_view_request_page_2, 'user1')

    assert response.status_code == 200
    assert b'Content 1' in response.content
    assert b'Content 2' not in response.content
    assert b'Content 3' in response.content
    assert b'Content 4' not in response.content
    assert b'Content 5' not in response.content
    assert b'Content 6' not in response.content
    assert b'Title 1' in response.content
    assert b'Title 2' not in response.content
    assert b'Title 3' in response.content
    assert b'Title 4' not in response.content
    assert b'Title 5' in response.content
    assert b'Title 6' not in response.content


def test_comment_view_known_user_get(comment_view_user_get_request):
    from post.views import comment_view

    request = comment_view(comment_view_user_get_request, 'dng101', '2018-01-15', 'slug-1')

    assert request.status_code == 200
    assert b'<label for="id_comment">Comment:</label> <textarea class="tinymce4-editor" ' \
           b'cols="40" id="id_comment" maxlength="10000" name="comment" placeholder="hello" ' \
           b'rows="10" required>' in request.content
    assert b'<input type="email" name="email" value="user1@address.com" class="" ' \
           b'placeholder="Email Address" maxlength="50" id="id_email">' in request.content


def test_comment_view_anonymous_user_get(comment_view_anonymous_get_request, six_posts):
    from post.views import comment_view

    request = comment_view(comment_view_anonymous_get_request, 'dng101', '2018-01-15', 'slug-1')

    assert request.status_code == 200
    assert b'<label for="id_comment">Comment:</label> <textarea class="tinymce4-editor" ' \
           b'cols="40" id="id_comment" maxlength="10000" name="comment" placeholder="hello" ' \
           b'rows="10" required>' in request.content


def test_comment_view_known_user_post(comment_view_user_post_request):
    from post.models import PostComment
    from post.views import comment_view

    request = comment_view(comment_view_user_post_request, 'dng101', '2018-01-15', 'slug-1')
    comment = PostComment.objects.get(pk=3)

    assert request.status_code == 302
    assert request.url == '/dng101/2018-01-15/slug-1/'
    assert comment.comment == "Here's a comment!"


def test_comment_view_anonymous_user_post(comment_view_anonymous_post_request, six_posts):
    from post.models import PostComment
    from post.views import comment_view

    request = comment_view(comment_view_anonymous_post_request, 'dng101', '2018-01-15', 'slug-1')
    comment = PostComment.objects.get(pk=3)

    assert request.status_code == 302
    assert request.url == '/dng101/2018-01-15/slug-1/'
    assert comment.comment == "Here's a comment!"


def test_comment_view_invalid_form_post(comment_view_user_post_request):
    from post.models import PostComment
    from post.views import comment_view

    with patch('django.forms.forms.BaseForm.is_valid', return_value=False):
        request = comment_view(comment_view_user_post_request, 'dng101', '2018-01-15', 'slug-1')

    # Then: the request shouldn't be redirected and searching
    # for the pk that a new post would have had doesn't exist
    assert request.status_code == 200
    with pytest.raises(PostComment.DoesNotExist):
        PostComment.objects.get(pk=3)


def test_user_post_list_user_not_found(home_view_request_page_2, six_posts):
    from post.views import user_post_list_view
    from django.http.response import Http404

    with pytest.raises(Http404):
        user_post_list_view(home_view_request_page_2, 'not-user')


def test_update_comment_view_not_logged_in(update_comment_not_logged_in_get_request, six_posts):
    from post.views import update_comment_view

    request = update_comment_view(update_comment_not_logged_in_get_request,
                                  'DNG101', '2018-01-15', 'slug-1')

    assert request.status_code == 302
    assert request.url == '/account/login/?next=/dng101/2018-03-15/slug-1/update_comment/'


def test_update_comment_view_wrong_user(update_comment_wrong_user_get_request, six_posts):
    from post.views import update_comment_view

    with pytest.raises(PermissionDenied):
        update_comment_view(update_comment_wrong_user_get_request,
                            'DNG101', '2018-01-15', 'slug-1')


def test_update_comment_view_author_get(update_comment_author_get_request, six_posts):
    from post.views import update_comment_view

    request = update_comment_view(update_comment_author_get_request,
                                  'DNG101', '2018-01-15', 'slug-1')

    assert request.status_code == 200
    assert b"<p>Here's a comment on the first comment</p>" in request.content


def test_update_comment_view_editor_get(update_comment_editor_get_request, six_posts):
    from post.views import update_comment_view

    request = update_comment_view(update_comment_editor_get_request,
                                  'DNG101', '2018-01-15', 'slug-1')

    assert request.status_code == 200
    assert b"<p>Here's a comment on the first comment</p>" in request.content


def test_update_comment_view_invalid_comment_post(update_comment_invalid_comment_post_request,
                                                  six_posts):
    from post.views import update_comment_view

    with patch('django.forms.forms.BaseForm.is_valid', return_value=False):
        request = update_comment_view(update_comment_invalid_comment_post_request,
                                      'DNG101', '2018-01-15', 'slug-1')

    assert request.status_code == 200
    assert b"It failed, hard." in request.content


def test_update_comment_view_post(update_comment_post_request, six_posts):
    from post.models import PostComment
    from post.views import update_comment_view

    request = update_comment_view(update_comment_post_request,
                                  'DNG101', '2018-01-15', 'slug-1')

    actual_saved_comment = PostComment.objects.get(pk=2).comment

    assert request.status_code == 302
    assert request.url == '/DNG101/2018-01-15/slug-1/'
    assert actual_saved_comment == "Here's an updated comment!!"


def test_category_view_page_1(home_view_request, six_posts):
    from post.views import root_view

    with patch('post.views.pagination_count', 2):
        response = root_view(home_view_request, 'dng101')

    assert response.status_code == 200
    assert b'Content 1' not in response.content
    assert b'Content 2' in response.content
    assert b'Content 3' in response.content
    assert b'Content 4' not in response.content
    assert b'Content 5' not in response.content
    assert b'Title 1' in response.content
    assert b'Title 2' in response.content
    assert b'Title 3' in response.content
    assert b'Title 4' in response.content
    assert b'Title 5' in response.content


def test_category_view_page_2(home_view_request_page_2, six_posts):
    from post.views import root_view

    with patch('post.views.pagination_count', 2):
        response = root_view(home_view_request_page_2, 'dng101')

    assert response.status_code == 200
    assert b'Content 1' in response.content
    assert b'Content 2' not in response.content
    assert b'Content 3' not in response.content
    assert b'Content 4' not in response.content
    assert b'Content 5' not in response.content
    assert b'Title 1' in response.content
    assert b'Title 2' in response.content
    assert b'Title 3' in response.content
    assert b'Title 4' in response.content
    assert b'Title 5' in response.content
