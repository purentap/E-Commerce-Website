from django.urls import path
from api import views
from rest_framework.authtoken.views import ObtainAuthToken
from .views import *


app_name = "api"
urlpatterns = [
	path('example/', UserRecordView.as_view(), name='users'),
    path("obtain-token/", ObtainAuthToken.as_view(), name="obtain-token"),
    path('products/', ProductRecordView.as_view(), name='products'),
    path('product-search/', ProductCategoryList.as_view(), name='genre'),

]
