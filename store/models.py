from django.db import models
from register.forms import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete =  models.CASCADE, null = True , blank = True)
    

class Product(models.Model):
    album_name = models.CharField(max_length=200, blank=False)
    artist_name = models.CharField(max_length=200, blank=False)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return(self.album_name)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null = True)
    order_date = models.DateTimeField(auto_now_add=True)
    isComplete = models.BooleanField(default=False, null = True, blank = False)
    transaction_id = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null= True)
    quantity = models.IntegerField(default = 0, null= True , blank = True)
    date_added =    models.DateTimeField(auto_now_add=True)
    
    

####SHIPPING ADDRESS YAZILACAK!! 