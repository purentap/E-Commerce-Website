from django.db import models
from register.forms import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

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
    onDiscount = models.BooleanField(default= False)
    image = models.ImageField(blank=True, null=True)


    #average rating score of all given ratings of orderitem

    @property
    def average_rating(self):
        return self.rating.aggregate(average_rating= Avg('rating'))['average_rating']
    

    def __str__(self):
        return(self.album_name)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    isComplete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, blank=False)
    class Status(models.IntegerChoices):
        PROCESSING = 1
        INTRANSIT = 2
        DELIVERED = 3
    status = models.IntegerField(choices=Status.choices, default=1)

    def __str__(self):
        return str(self.id)
    
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
    #if order.isComplete = True, customer is able to rate the product on my orders page
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='rating')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, null=True,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
        )


    def __str__(self):
        return str(self.id)
    
    @property
    def getTotal(self):
        totalCost = self.product.price * self.quantity
        return totalCost


class ShippingAdress(models.Model):
    customer = models.ForeignKey(
    User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    country =  models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


# MUST ENCRYPT, MIGHT GET DEPRECATED, NOT A GOOD IDEA TO KEEP IN DATABASE
class CreditCard(models.Model):
    customerID = models.ForeignKey(
    User, on_delete=models.SET_NULL, blank=True, null=True)
    cardName = models.CharField(max_length=100, null=True)
    cardAlias = models.CharField(max_length=100, null=True, blank=True) #BUNE 
    cardNumber = models.CharField(max_length=19, null=True, blank=False)
    # Might get modified
    #exprDate = models.DateField()
    exprDate = models.CharField(max_length=100, null=True, blank=False)
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=500)
    approval = models.IntegerField(choices=Approval.choices, default=1)

    def __str__(self):
        return '%s - %s - %s %s' %(self.product.artist_name,self.product.album_name, self.user.first_name,  self.user.last_name)



