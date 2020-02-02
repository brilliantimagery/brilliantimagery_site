from django.urls import reverse, resolve


class TestModelUrls:

    def test_create_new_url(self):
        path = reverse('post:create-new')
        assert resolve(path).view_name == 'post:create-new'

    def test_slugged_username_url(self):
        path = reverse('post:user-posts', kwargs={'username': '_'})
        assert resolve(path).view_name == 'post:user-posts'

    def test_root_view_url(self):
        path = reverse('post-slugged:root-view', kwargs={'root_slug': '_'})
        assert resolve(path).view_name == 'post-slugged:root-view'

    def test_detail_view_url(self):
        path = reverse('post-slugged:detail-view', kwargs={'root_slug': '_', 'date_slug': '_', 'post_slug': '_'})
        assert resolve(path).view_name == 'post-slugged:detail-view'

    def test_delete_url(self):
        path = reverse('post-slugged:delete', kwargs={'root_slug': '_', 'date_slug': '_', 'post_slug': '_'})
        assert resolve(path).view_name == 'post-slugged:delete'

    def test_update_url(self):
        path = reverse('post-slugged:update', kwargs={'root_slug': '_', 'date_slug': '_', 'post_slug': '_'})
        assert resolve(path).view_name == 'post-slugged:update'

    def test_comment_url(self):
        path = reverse('post-slugged:comment', kwargs={'root_slug': '_', 'date_slug': '_', 'post_slug': '_'})
        assert resolve(path).view_name == 'post-slugged:comment'

    def test_update_comment_url(self):
        path = reverse('post-slugged:update_comment', kwargs={'root_slug': '_', 'date_slug': '_', 'post_slug': '_'})
        assert resolve(path).view_name == 'post-slugged:update_comment'