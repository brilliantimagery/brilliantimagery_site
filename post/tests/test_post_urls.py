from django.urls import reverse, resolve


class TestModelUrls:

    def test_create_new_url(self):
        path = reverse('post:create-new')
        assert resolve(path).view_name == 'post:create-new'

    def test_slugged_username_url(self):
        path = reverse('post:user-posts', kwargs={'username': '_'})
        assert resolve(path).view_name == 'post:user-posts'

    def test_category_view_url(self):
        path = reverse('post-slugged:category-view', kwargs={'slug_category': '_'})
        assert resolve(path).view_name == 'post-slugged:category-view'

    def test_detail_view_url(self):
        path = reverse('post-slugged:detail-view', kwargs={'slug_category': '_', 'date_slug': '_', 'slug_post': '_'})
        assert resolve(path).view_name == 'post-slugged:detail-view'

    def test_delete_url(self):
        path = reverse('post-slugged:delete', kwargs={'slug_category': '_', 'date_slug': '_', 'slug_post': '_'})
        assert resolve(path).view_name == 'post-slugged:delete'

    def test_update_url(self):
        path = reverse('post-slugged:update', kwargs={'slug_category': '_', 'date_slug': '_', 'slug_post': '_'})
        assert resolve(path).view_name == 'post-slugged:update'

    def test_comment_url(self):
        path = reverse('post-slugged:comment', kwargs={'slug_category': '_', 'date_slug': '_', 'slug_post': '_'})
        assert resolve(path).view_name == 'post-slugged:comment'

    def test_update_comment_url(self):
        path = reverse('post-slugged:update_comment', kwargs={'slug_category': '_', 'date_slug': '_', 'slug_post': '_'})
        assert resolve(path).view_name == 'post-slugged:update_comment'