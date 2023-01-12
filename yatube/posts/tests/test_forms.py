import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from ..models import Group, Post, User, Comment
from ..forms import PostForm


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.form = PostForm()

        cls.user = User.objects.create_user(username='TestAuthor')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=CreateFormTest.group
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        post_count = Post.objects.count()
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
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': 'TestAuthor'})
        )
        self.assertTrue(Post.objects.filter(
            text=form_data['text'],
            group=form_data['group'],
            image='posts/small.gif'
        ).exists())
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_post_edit_form(self):
        post_ex = Post.objects.get(id=1)
        form_data = {
            'text': 'Измененный текст',
            'group': self.group.id
        }
        post_ex.text = form_data['text']
        post_ex.group = self.group
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': '1'})
        )
        post_upd = Post.objects.get(id=1)
        self.assertEqual(post_ex.text, post_upd.text)
        self.assertEqual(post_ex.pub_date, post_upd.pub_date)
        self.assertEqual(post_ex.author_id, post_upd.author_id)
        self.assertEqual(post_ex.group_id, post_upd.group_id)
        self.assertEqual(post_ex.image, post_upd.image)

    def test_create_comment(self):
        form_data = {
            'text': 'Тестовый комментарий'
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True
        )
        rev = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': '1'})
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': '1'})
        )
        self.assertTrue(Comment.objects.filter(
            text=form_data['text']).exists()
        )
        self.assertContains(
            rev,
            form_data['text'],
            status_code=200
        )
