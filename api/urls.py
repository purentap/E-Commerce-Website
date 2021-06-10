from django.urls import path, include
from api import views
from rest_framework.authtoken.views import ObtainAuthToken
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'order-item', views.OrderItemViewSet)
router.register(r'shipping-address', views.ShippingAddressViewSet)
router.register(r'credit-card', views.CreditCardViewSet)
router.register(r'comments', views.CommentViewSet)



app_name = "api"
urlpatterns = [
    path('example/', UserProfileInfo.as_view(), name='username'),
    path('order-info/', OrderInfo.as_view(), name='customer'),
    path('users/', UserRecordView.as_view(), name='users'),
    path('product-user-search/', ProductSearchList.as_view()),


    #path('order-detail-search/', OrderItemInfo.as_view(), name='order'),

    #path('order-search/', PurchaseList.as_view(), name='customer'),
    path("obtain-token/", ObtainAuthToken.as_view(), name="obtain-token"),
    path("obtain-token/", ObtainAuthToken.as_view(), name="obtain-token"),
    path('products/', ProductRecordView.as_view(), name='products'),
    path('product-search/', ProductCategoryList.as_view(), name='genre'),
    #path('order-item/', OrderDetailList.as_view(), name='order-item'),
    #path('<str:username>/', PurchaseList.as_view(), name='customer'),
    path('', include(router.urls)),
    ]
