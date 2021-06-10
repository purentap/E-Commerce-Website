from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem, ShippingAdress, CreditCard, Comment, Refund
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import status, generics, filters
import json


# class OrderRecordView(APIView):
#     def get(self, request, format= None):
#         orders = Order.objects.all()
#         serializer = OrderSerializer(orders, many= True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = OrderSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(
#             {
#                 "error": True,
#                 "error_msg": serializer.error_messages,
#             },

#             status=status.HTTP_400_BAD_REQUEST)

class SlSoftDeleteMixin(mixins.DestroyModelMixin):
    """ As we are deleting soft"""

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('uuid'))
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    #permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductRecordView(APIView):
    def get(self, request, format= None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many= True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },

            status=status.HTTP_400_BAD_REQUEST)

class ProductCategoryList(generics.ListAPIView):
    model = Product
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['genre']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductSearchList(generics.ListAPIView):
    model = Product
    search_fields = ['album_name', 'artist_name']
    filter_backends = (filters.SearchFilter, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserProfileInfo(generics.ListAPIView):
    model = User
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['username']
    serializer_class = UserSerializer
    queryset = User.objects.all()


class OrderInfo(generics.ListAPIView):
    model = Order
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['customer']
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderItemInfo(generics.ListAPIView):
    model = OrderItem
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['customer']
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

# class UserProfileInfo(generics.ListAPIView):
#     model = User
#     filter_backends = [DjangoFilterBackend,]
#     filterset_fields = ['username']
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

# class PurchaseList(generics.ListAPIView):
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Order.objects.all()
#         username = self.request.query_params.get('username', None)
#         if username is not None:
#             queryset = queryset.filter(user__username=username)
#         return queryset

class OrderDetailList(generics.ListAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OrderItem.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset


# class UserByOrdererList(generics.ListAPIView):
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         orderer = self.kwargs['Order']
#         return User.objects.filter(Order= orderer)

    # def get(self, format=None):
    #     queryset = Order.objects.filter(customer__username=self.request.user).first()
    #     serializer = OrderSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # model = Order
    # user_info = Order.objects.filter(username__customer=self.request.user).first()

    # filter_backends = [DjangoFilterBackend,]
    # filterset_fields = ['customer']
    # serializer_class = OrderSerializer
    # queryset = Order.objects.all()


class OrderItemViewSet(viewsets.ModelViewSet): 
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemDetailSerializer #OrderItems
    detail_serializer_class = OrderItemDetailSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    ordering_fields = '__all__'
    #depth = 1

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         if hasattr(self, 'detail_serializer_class'):
    #             return self.detail_serializer_class
    #     return super().get_serializer_class()

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        product = self.request.query_params.get('product', None)
        order = self.request.query_params.get('order', None)
        order_id = self.request.query_params.get('order_id', None)
        if product is not None:
            product = product.title()
            queryset = queryset.filter(product__album_name=product)
        if order is not None:
            order = order.title()
            queryset = queryset.filter(order__customer=order)
        if order_id is not None:
            order_id = order_id.title()
            queryset = queryset.filter(order__id= order_id)
        return queryset

    def create(self, validated_data):
        message = validated_data.data.pop('message_type')
        if message == "NewOrderItem":
            event =  validated_data.data.pop('event')
            product = event.pop('product')
            order = event.pop('order')
            customer = order.pop('customer')
            username = customer.pop('username')
            customer = get_user_model().objects.get_or_create(username=username)[0]
            order , created = Order.objects.get_or_create(customer=customer, isComplete=False)
            product = Product.objects.get(**product)
            order_item = OrderItem.objects.create(**event, product=product, order=order)
            return Response(status=status.HTTP_201_CREATED)
        #Update can made through put request too
        elif message == "UpdateOrderItem":
            event =  validated_data.data.pop('event')
            order = event.pop('order')
            edit = Order.objects.get(id = order['id'])
            edit.isComplete = order['isComplete']
            edit.save()
            return Response(status=status.HTTP_201_CREATED)

        elif message == "ChangeQuantity":
            event =  validated_data.data.pop('event')
            order = event.pop('order')
            edit = OrderItem.objects.get(id = event['id'])
            edit.quantity = event['quantity']
            edit.save()
            return Response(status=status.HTTP_201_CREATED)

        elif message == "AddRating":
            event =  validated_data.data.pop('event')
            order = event.pop('order')
            edit = OrderItem.objects.get(id = event['id'])
            edit.rating = event['rating']
            edit.save()
            return Response(status=status.HTTP_201_CREATED)



        elif message == "DeleteOrderItem":
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        #instance.is_active = False
        #instance.save()
        instance.delete() #not the correct way
        return Response(status=status.HTTP_204_NO_CONTENT)
        #probably order item pk is a mustS
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        #instance.is_active = False
        #instance.save()
        instance.delete() #not the correct way
        return Response(status=status.HTTP_204_NO_CONTENT)
        #probably order item pk is a mustS
class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAdress.objects.all()
    serializer_class = ShippingAddressSerializer 
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    ordering_fields = '__all__'
    depth = 1

    def create(self, validated_data):
        message = validated_data.data.pop('message_type')
        if message == "PostShipping":
            event = validated_data.data.pop('event');
            customer = event.pop('customer')
            username = customer.pop('username')
            order = event.pop('order')
            customer = get_user_model().objects.get_or_create(username=username)[0]
            order = Order.objects.get(customer=customer, isComplete=False)
            shipping_address = ShippingAdress.objects.create(**event, customer=customer, order=order)
            return Response(status=status.HTTP_201_CREATED)
            
        elif message == "PurchaseSuccess":
            event = validated_data.data.pop('event');
            customer = event.pop('customer')
            username = customer.pop('username')
            order = event.pop('order')
            customer = get_user_model().objects.get_or_create(username=username)[0]
            order = Order.objects.get(customer=customer, isComplete=False)
            order.isComplete = True
            order.save()
            return Response(status=status.HTTP_201_CREATED)



class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer 
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    ordering_fields = '__all__'
    depth = 1

    def create(self, validated_data):
        event = validated_data.data.pop('event')
        customer = event.pop('customerID')
        username = customer.pop('username')
        customer = get_user_model().objects.get_or_create(username=username)[0]
        creditcard = CreditCard.objects.create(**event, customerID=customer)
        return Response(status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class= CommentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    ordering_fields = '__all__'
    depth = 1

    def get_queryset(self):
        queryset = Comment.objects.all()
        #filter only allowed comments to be shown
        product = self.request.query_params.get('product', None)
        if product is not None:
            product = product.title()
            queryset = queryset.filter(product__album_name=product)
        return queryset

    def create(self, validated_data):
        #post comments as approval in flutter = 1
        event = validated_data.data.pop('event')
        product = event.pop('product')
        user = event.pop('user')
        username = user.pop('username')
        user = get_user_model().objects.get_or_create(username=username)[0]
        product = Product.objects.get(**product)
        comment = Comment.objects.create(**event, product=product, user=user)
        return Response(status=status.HTTP_201_CREATED)


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class= RefundSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    ordering_fields = '__all__'
    depth = 1

    def get_queryset(self):
        queryset = Refund.objects.all()
        #filter only allowed comments to be shown
        order_item = self.request.query_params.get('order_item', None)
        if order_item is not None:
            order_item = order_item.title()
            queryset = queryset.filter(order_item__product__album_name=order_item)
        return queryset

    def create(self, validated_data):
        #post comments as approval in flutter = 1
        event = validated_data.data.pop('event')
        item = event.pop('order_item')
        item_id = item.pop('id')
        item = OrderItem.objects.get(**event, pk=item_id)
        serializer_class= RefundSerializer(item, many=False)
        refund, created = Refund.objects.get_or_create(order_item = item)
        refund.onDiscount = item.product.onDiscount
        refund.price = item.product.price
        refund.quantity = item.quantity
        refund.total = item.getTotal
        refund.save()
        item.refund_request = True
        item.save()
        return Response(status=status.HTTP_201_CREATED)
