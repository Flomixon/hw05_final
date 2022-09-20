from django.core.cache import cache
from django.test import TestCase, Client
from ..models import Group, Post, User


class URLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestAuthor')
        Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_page_404(self):
        response = self.guest_client.get('test')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')

    def test_urls_uses_correct_template(self):
        cache.clear()
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/TestAuthor/': 'posts/profile.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_correct_urls_authorized(self):
        urls_name = (
            '/',
            '/group/test_slug/',
            '/profile/TestAuthor/',
            '/posts/1/edit/',
            '/posts/1/',
            '/create/'
        )
        for url in urls_name:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_correct_urls_guest(self):
        urls_name = (
            '/',
            '/group/test_slug/',
            '/profile/TestAuthor/',
            '/posts/1/'
        )
        for url in urls_name:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_correct_urls_guest(self):
        response = self.guest_client.get('/create/')
        self.assertRedirects(response, ('/auth/login/?next=/create/'))

    def test_post_edit(self):
        response = self.guest_client.get('/posts/1/edit/')
        self.assertRedirects(response, ('/posts/1/'))
