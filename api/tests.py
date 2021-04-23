# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="supersecretpassword",
        )
    def test_created_token_successfully(self):
        token = Token.objects.get(user=self.user)
        self.assertTrue(hasattr(self.user, "auth_token"))
        self.assertEqual(token, self.user.auth_token)

def test_user_obtain_token_successfully_and_authorized(self):
        from rest_framework.test import APIClient
        from django.urls import reverse
        from rest_framework import status
        client = APIClient()
        payload = {"username": "test", "password": "supersecretpassword"}
        token_request = client.post(reverse("api:obtain-token"), payload)
        self.assertEqual(token_request.status_code, status.HTTP_200_OK)
        client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
        example_request = client.get(reverse("api:example"))
        self.assertEqual(example_request.status_code, status.HTTP_200_OK)