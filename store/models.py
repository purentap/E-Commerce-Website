from django.db import models
from register.forms import User

# Create your models here.
# class Customer(models.Model):
#    user = models.OneToOneField(User, on_delete =  models.CASCADE, null = True , blank = True)


class Product(models.Model):
    model_no = models.CharField(max_length=200, blank=True, null=True)
    album_name = models.CharField(max_length=200, blank=False)
    artist_name = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)
    warranty = models.CharField(max_length=200, blank=True, null=True)
    distributor = models.CharField(max_length=200, blank=True, null=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return(self.album_name)


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    isComplete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAdress(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


# MUST ENCRYPT, MIGHT GET DEPRECATED, NOT A GOOD IDEA TO KEEP IN DATABASE
class CreditCard(models.Model):
    customerID = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    cardAlias = models.CharField(max_length=100, null=True, blank=True)
    cardName = models.CharField(max_length=100, null=True)
    cardNumber = models.CharField(max_length=19, null=True, blank=True)
    # Might get modified
    exprDate = models.DateField()
    exprMon = models.CharField()
    exprDay = models.CharField()
    #
    brand = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.cardAlias)
