from django.test import TestCase
from .models import *
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from . import views
    
class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('store'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('store'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

class ProductModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Product.objects.create(album_name='album1', artist_name='artist1', price=100)

    def test_album_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('album_name').verbose_name
        self.assertEqual(field_label, 'album name')

    def test_artist_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('artist_name').verbose_name
        self.assertEqual(field_label, 'artist name')

    def test_album_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('album_name').max_length
        self.assertEqual(max_length, 200)

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()
        Order.objects.create(customer=self.user,transaction_id='123')

    def test_transaction_id(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('transaction_id').verbose_name
        self.assertEqual(field_label, 'transaction id')

    def test_transaction_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('transaction_id').max_length
        self.assertEqual(max_length, 200)

class OrderItemModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()
        
        OrderItem.objects.create(order=Order.objects.create(customer=self.user,transaction_id='123'),
        product=Product.objects.create(album_name='album1', artist_name='artist1', price=100))

    def test_orderitem_exists(self):
        item_count = Order.objects.all().count()
        self.assertEqual(item_count, 1)


class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pwd(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
    
