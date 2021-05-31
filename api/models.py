from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

# Create your models here

class Product(models.Model):
    model_no = models.CharField(max_length=200, blank=True, null=True)
    album_name = models.CharField(max_length=200, blank=True, null=True)
    artist_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)
    warranty = models.CharField(max_length=200, blank=True, null=True)
    distributor = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=200, blank=True, null=True)
    stock = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)


    def get_absolute_url(self):
        return reverse('product-detail-view', args[str(self.id)])

    @property
    def average_rating(self):
        return self.rating.aggregate(average_rating= Avg('rating'))['average_rating']
    

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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='rating')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
        )

    def __str__(self):
        return str(self.id)

    def current_order(self):
        return Order.objects.filter(order=self.order)

    @property
    def getTotal(self):
        totalCost = self.product.price * self.quantity
        return totalCost

#runner = order item
#event = product
#market = order


class ShippingAdress(models.Model):
    customer = models.ForeignKey(
    User, on_delete=models.SET_NULL, blank=True, null=True, related_name = 'customer_shipping')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    country =  models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class CreditCard(models.Model):
    customerID = models.ForeignKey(
    User, on_delete=models.SET_NULL, blank=True, null=True, related_name= 'customer_credit')
    cardName = models.CharField(max_length=100, null=True)
    cardAlias = models.CharField(max_length=100, null=True, blank=True) #BUNE 
    cardNumber = models.CharField(max_length=19, null=False, blank=True)
    # Might get modified
    #exprDate = models.DateField()
    exprDate = models.CharField(max_length=100, null=False, blank=True)
    
    #
    #brand = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.cardAlias)

class Comment(models.Model):
    class Approval(models.IntegerChoices):
        PENDING = 1
        APPROVED = 2
        DISAPPROVED = 3

    product = models.ForeignKey (Product, related_name = "comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comment_user")
    date_added = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=500)
    approval = models.IntegerField(choices=Approval.choices, default=1)

    def __str__(self):
        return '%s - %s - %s %s' %(self.product.artist_name,self.product.album_name, self.user.first_name,  self.user.last_name)

