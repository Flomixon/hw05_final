import shutil
import tempfile
from django.core.cache import cache
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms
from ..models import Group, Post, User


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.user = User.objects.create_user(username='TestAuthor')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.guest_client = Client()
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=ViewsTest.group
            )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_first_page_contains_ten_records(self):
        cache.clear()
        response = self.client.get(reverse('posts:posts'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:posts') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_pages_correct_template(self):
        cache.clear()
        template_pages_names = {
            reverse('posts:posts'): 'posts/index.html',
            (reverse('posts:group_list', kwargs={'slug': 'test_slug'})):
                'posts/group_list.html',
            (reverse('posts:profile', kwargs={'username': 'TestAuthor'})):
                'posts/profile.html',
            (reverse('posts:post_edit', kwargs={'post_id': '1'})):
                'posts/create_post.html',
            (reverse('posts:post_detail', kwargs={'post_id': '1'})):
                'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in template_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_show_correct_context_with_pagin(self):
        cache.clear()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        Post.objects.create(
            author=self.user,
            text='Тестовый пост',
            group=ViewsTest.group,
            image=uploaded
        )
        view_urls = (
            reverse('posts:posts'),
            (reverse('posts:group_list', kwargs={'slug': 'test_slug'})),
            (reverse('posts:profile', kwargs={'username': 'TestAuthor'})),
        )
        for reverse_name in view_urls:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_obj = response.context['page_obj'][0]
                text_0 = first_obj.text
                author_0 = first_obj.author
                group_0 = first_obj.group
                image_0 = first_obj.image
                self.assertEqual(text_0, 'Тестовый пост')
                self.assertEqual(author_0, self.user)
                self.assertEqual(group_0, self.group)
                self.assertEqual(image_0, 'posts/small.gif')
        id = Post.objects.get(image='posts/small.gif')
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': id.id}
            )
        )
        first_obj = response.context.get('post')
        text_0 = first_obj.text
        author_0 = first_obj.author
        group_0 = first_obj.group
        image_0 = first_obj.image
        self.assertEqual(text_0, 'Тестовый пост')
        self.assertEqual(author_0, self.user)
        self.assertEqual(group_0, self.group)
        self.assertEqual(image_0, 'posts/small.gif')

    def test_form_creat_post(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_comment_form(self):
        rev = reverse('posts:post_detail', kwargs={'post_id': '1'})
        response = self.authorized_client.get(rev)
        self.assertIsInstance(
            response.context.get('form').fields.get('text'),
            forms.fields.CharField
        )
        response = self.guest_client.get(rev)
        self.assertNotContains(
            response,
            'Добавить комментарий:',
            status_code=200
        )

    def test_cache_index(self):
        Post.objects.create(
            author=self.user,
            text='Тест кеша'
        )
        response = self.guest_client.get(reverse('posts:posts'))
        cache_ = response.content
        Post.objects.filter(text='Тест кеша').delete()
        response = self.guest_client.get(reverse('posts:posts'))
        self.assertEqual(response.content, cache_)
        cache.clear()
        response = self.guest_client.get(reverse('posts:posts'))
        self.assertNotEqual(response.content, cache_)
