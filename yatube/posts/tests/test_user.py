from django.test import Client, TestCase
from django.urls import reverse
from ..models import User


class UserTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_signup_form(self):
        form_data = {
            'first_name': 'TestName',
            'last_name': 'TestName',
            'username': 'TestUser',
            'email': 'test@tastmail.com',
            'password1': 'Baguvix123',
            'password2': 'Baguvix123',
        }
        user_count = User.objects.all().count()
        guest_client = Client()
        guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(User.objects.all().count(), user_count + 1)
        self.assertTrue(User.objects.filter(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            username=form_data['username'],
            email=form_data['email'],
        ).exists())
