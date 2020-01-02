from mixer.backend.django import mixer
import pytest


def test_postcategory_str(db):
    category = 'Hello!!! Hello again.'
    post_category = mixer.blend('post.PostCategory', category=category)

    actual = str(post_category)
    expected = category

    assert actual == expected


def test_post_str(db):
    import datetime

    title = 'Title'
    publish_date = datetime.datetime(2020, 8, 12)
    post = mixer.blend('post.Post', title=title, publish_date=publish_date)

    actual = str(post)
    expected = f'Title - 2020-08-12'

    assert actual == expected


def test_post_content_summary_with_paragraph_tags(db):
    content = '<p>Hello!!!</p> <p>Hello again.</p>'
    post = mixer.blend('post.Post', content=content)

    actual = post.content_summary
    expected = '<p>Hello!!!</p>'

    assert actual == expected


def test_post_content_summary_without_paragraph_tags(db):
    content = 'Hello!!! Hello again.'
    post = mixer.blend('post.Post', content=content)

    actual = post.content_summary
    expected = content

    assert actual == expected


# def test_post_get_absolute_url(self):
#     category = mixer.blend('post.Cat')
#     slug_category = 'category'
#     date_slug
#     post = mixer.blend('post.Post', content=content)
#
#     actual = post.content_summary
#     expected = content
#
#     assert actual == expected

def test_postcomment_str(db):
    import datetime

    comment = "Here's a string that's more than one hundred characters long. " \
              "It won't really fit on one line so it breaks pep 8 rules."
    post_comment = mixer.blend('post.PostComment', comment=comment)

    actual = str(post_comment)
    expected = "Here's a string that's more than one hundred characters long. " \
               "It won't really fit on one line so it "

    assert actual == expected
