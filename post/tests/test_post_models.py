from mixer.backend.django import mixer


def test_postcategory_str(db):
    category = 'Hello!!! Hello again.'
    post_category = mixer.blend('post.PostCategory', name=category)

    actual = str(post_category)
    expected = category

    assert actual == expected


def test_post_str(db):
    import datetime

    title = 'Title'
    publish_date = datetime.datetime(2020, 8, 12)

    from django.contrib.auth.models import User
    mixer.blend(User)
    mixer.blend('post.PostCategory')
    post = mixer.blend('post.Post', title=title, publish_date=publish_date)

    actual = str(post)
    expected = f'Title - 2020-08-12'

    assert actual == expected


def test_post_content_summary_with_paragraph_tags(post_w_path_content):
    post, expected_path, expected_content = post_w_path_content

    actual = post.content_summary
    expected = expected_content.split(' ')[0]

    assert actual == expected


def test_post_content_summary_without_paragraph_tags(post_w_path_content):
    post, expected_path, expected_content = post_w_path_content

    content = 'Hello!!! Hello again.'
    post.content = content

    actual = post.content_summary
    expected = content

    assert actual == expected


def test_post_get_absolute_url(post_w_path_content):
    post, expected_path, expected_content = post_w_path_content
    actual_path = post.get_absolute_url()

    assert actual_path == expected_path


def test_postcomment_str(db):
    comment = "Here's a string that's more than one hundred characters long. " \
              "It won't really fit on one line so it breaks pep 8 rules."
    from django.contrib.auth.models import User
    mixer.blend(User)
    mixer.blend('post.PostCategory')
    mixer.blend('post.Post')
    post_comment = mixer.blend('post.PostComment', comment=comment)

    actual = str(post_comment)
    expected = "Here's a string that's more than one hundred characters long. " \
               "It won't really fit on one line so it "

    assert actual == expected
