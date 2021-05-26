from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import *


    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = Order.objects.all()
    #     username = self.request.query_params.get('username', None)
    #     if username is not None:
    #         queryset = queryset.filter(user__username=username)
    #     return queryset


#selection: order 
#Match = order item
#Market = user
#no foreign key on user

#Sport = product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('model_no','album_name', 'artist_name', 'description', 'genre', 'warranty','distributor', 'price', 'stock', 'image', 'average_rating')


class OrderOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('customer','order_date', 'isComplete', 'transaction_id')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = ('id','customer','order_date', 'isComplete', 'transaction_id')
        depth = 1



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id','product','order', 'quantity', 'date_added', 'rating')
        depth = 1



class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()
    class Meta:
        model = OrderItem
        fields = ('id','product','order', 'quantity', 'date_added', 'rating')

    # def create(self, validated_data):
    #     product = self.context['request'].product[0]
    #     order = self.context['request'].order[0]
    #     customer = self.context['request'].customer[0]
    #     order_item = OrderItem.objects.create(product=product, order=order, customer=customer, **validated_data)
    #     return order_item
        # order = validated_data.pop('order')[0]
        # customer = order.pop('user')
        # question = OrderItem.objects.create(**validated_data)
        # return question

class ShippingAddressSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    order = OrderSerializer()
    class Meta:
        model = ShippingAdress
        fields = ('customer','order','address', 'city', 'state', 'zipcode', 'country', 'date_added')

class CreditCardSerializer(serializers.ModelSerializer):
    customerID = CustomerSerializer()
    class Meta:
        model = CreditCard
        fields = ('customerID','cardName','cardAlias', 'cardNumber', 'exprDate')

class CommentSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model= Comment
        fields = ('product', 'user', 'date_added', 'body', 'approval')