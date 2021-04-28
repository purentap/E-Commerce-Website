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
    onDiscount = models.BooleanField(default= False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return(self.album_name)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    isComplete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, blank=False)

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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        totalCost = self.product.price * self.quantity
        return totalCost


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
    exprMon = models.CharField(max_length=100)
    exprDay = models.CharField(max_length=100)
    #
    brand = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.cardAlias)
