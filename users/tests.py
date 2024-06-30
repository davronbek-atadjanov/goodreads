from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "Davronbek",
                "first_name": "Davronbek",
                "last_name": "Hasanov",
                "email": "hasanovdavronbek@gmail.com",
                "password": "Hasanov123"
        })

        user = User.objects.get(username="Davronbek")
        self.assertEqual(user.first_name, "Davronbek")
        self.assertEqual(user.last_name, "Hasanov")
        self.assertEqual(user.email, "hasanovdavronbek@gmail.com")
        self.assertTrue(user.check_password("Hasanov123"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data = {
                "first_name": "Davronbek",
                "email": "hasanov@gmail.com"
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response.context['form'], "username", "This field is required.")
        self.assertFormError(response.context['form'], "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Davronbek",
                "first_name": "Davronbek",
                "last_name": "Hasanov",
                "email": "hasanovdavronbek",
                "password": "Hasanov123"
        })

        user_count = User.objects.count()
        self.assertFormError(response.context['form'], "email", "Enter a valid email address.")

    def test_uniq_username(self):
        user = User.objects.create(username="Davronbek")
        user.set_password("Hsanov123")
        user.save()
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Davronbek",
                "first_name": "Davronbek",
                "last_name": "Hasanov",
                "email": "hasanovdavronbek",
                "password": "Hasanov123"
            })
        user = User.objects.count()
        self.assertEqual(user, 1)
        self.assertFormError(response.context['form'], 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def test_successful_login(self):
        db_user = User.objects.create(username="Davronbek")
        db_user.set_password("Hsanov123")
        db_user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Davronbek",
                "password": "Hsanov123"
            }
        )
        # login qilindi
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        db_user = User.objects.create(username="Davronbek")
        db_user.set_password("Hsanov123")
        db_user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "Hsanov123"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Davronbek",
                "password": "wrong-password"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_empty_username(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "",
                "password": "Hasanov"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
    def test_empty_password(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "Davronbek",
                "password": ""
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = User.objects.create(username="Davronbek", first_name="Hasanov", last_name="Davronbek", email="hasanov2@gmail.com")
        user.set_password("Hasanov123")
        user.save()

        self.client.login(username="Davronbek", password="Hasanov123")

        response = self.client.get(
            reverse("users:profile")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)