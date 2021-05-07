from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
        fields = ('model_no','album_name', 'artist_name', 'description', 'genre', 'warrantry','distributor', 'price', 'stock', 'image')


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


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    class Meta:
        model = Order
        fields = ('id','customer','order_date', 'isComplete', 'transaction_id')
        depth = 1



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product','order', 'quantity', 'date_added')


class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()
    class Meta:
        model = OrderItem
        fields = ('product','order', 'quantity', 'date_added')


