from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem
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
    depth = 1

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        product = self.request.query_params.get('product', None)
        order = self.request.query_params.get('order', None)
        if product is not None:
            product = product.title()
            queryset = queryset.filter(product__album_name=product)
        if order is not None:
            order = order.title()
            queryset = queryset.filter(order__customer=order)
        return queryset

    def create(self, request): #parse incoming request or add new order item
        message = request.data.pop('event')
        if message == "NewOrderItem":
            event = request.data.pop('event')
            product = event.pop('product')
            orders = event.pop('orders')[0] #only one order
            customer = orders.pop('order') #not sure about selections
            product = Product.objects.create(**product)
            orders = Order.objects.create(**orders, product=product) #not sure

            orders.customer.create(**user)
            order = Order.objects.create(**event, product=product, order=orders)
            return Response(status=status.HTTP_201_CREATED)


