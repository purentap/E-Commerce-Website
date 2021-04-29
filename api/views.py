from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from store.models import Product
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import status, generics, filters


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [IsAdminUser]

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

