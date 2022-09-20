from django.test import TestCase
from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_group_str(self):
        group = PostModelTest.group
        correct_str = group.title
        self.assertEqual(correct_str, str(group))

    def test_models_have_correct_post_str(self):
        post = PostModelTest.post
        correct_str = post.text[:15]
        self.assertEqual(correct_str, str(post))
