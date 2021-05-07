from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    model_no = models.CharField(max_length=200, blank=True, null=True)
    album_name = models.CharField(max_length=200, blank=True, null=True)
    artist_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)
    warrantry = models.CharField(max_length=200, blank=True, null=True)
    distributor = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=200, blank=True, null=True)
    stock = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('product-detail-view', args[str(self.id)])

    def __str__(self):
        return(self.album_name)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name = 'customer_user')
    order_date = models.DateTimeField(auto_now_add=True)
    isComplete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' | ' + self.product.album_name
    
    @property
    def getCartTotal(self): #returns total price of items in the order
        orderItems = self.orderitem_set.all()
        totalCost = sum([item.getTotal for item in orderItems])
        return totalCost

    @property
    def getCartItems(self): # returns amount of items in the order
        orderItems = self.orderitem_set.all()
        totalItems = sum([item.quantity for item in orderItems])
        return totalItems
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def current_order(self):
        return Order.objects.filter(order=self.order)

    @property
    def getTotal(self):
        totalCost = self.product.price * self.quantity
        return totalCost



#runner = order item
#event = product
#market = order

