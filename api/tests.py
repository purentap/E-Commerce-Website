# Create your tests here.
from django.urls import include, path
from django.test import TestCase
from django.contrib.auth.models import User
from .models import OrderItem, Order, Product
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient, URLPatternsTestCase
# class UserTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="test", password="supersecretpassword",
#         )
#     def test_created_token_successfully(self):
#         token = Token.objects.get(user=self.user)
#         self.assertTrue(hasattr(self.user, "auth_token"))
#         self.assertEqual(token, self.user.auth_token)

# def test_user_obtain_token_successfully_and_authorized(self):
#         from rest_framework.test import APIClient
#         from django.urls import reverse
#         from rest_framework import status
#         client = APIClient()
#         payload = {"username": "test", "password": "supersecretpassword"}
#         token_request = client.post(reverse("api:obtain-token"), payload)
#         self.assertEqual(token_request.status_code, status.HTTP_200_OK)
#         client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
#         example_request = client.get(reverse("api:example"))
#         self.assertEqual(example_request.status_code, status.HTTP_200_OK)

class OrderItemTests(APITestCase):
    def test_create_item(self):
        """
        Ensure we can create a new match object.
        """
        url = ('http://127.0.0.1:8000/api/order-items/')
        data = {
                 #"id": 8661032861909884224,
                 "message_type": "NewOrderItem",
                 "event": {
                     "quantity": 1,
                     "date_added": "2018-06-20 10:30:00",
                     "product": {
                         "model_no": "221",
                         "album_name": "Football",
                         "artist_name": "Football",
                         "description": "Football",
                         "genre": "pop",
                         "warrantry": "yes",
                         "distributor": "Eylo Records",
                         "price": "10",
                         "stock": "15",
                         "image": "image1.url",
                     },
                     "orders": [
                         {
                         "isComplete": True,
                         "transaction_id": "123"
                         "order_date": "2018-06-20 10:30:00",
                         "customer": [
                             {
                             "username": "bektur",
                             "first_name": "Eylul",
                             "last_name": "Bektur",
                             "email": "eylulspor@gmail.com",
                             },
                            ]
                        }
                     ]
                    }
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(OrderItem.objects.get().name, 'Positions')
