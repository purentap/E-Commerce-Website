from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = "store"),
    path('cart/', views.cart, name = "cart"),
    path('checkout/', views.checkout, name = "checkout"),
    path('account/', views.account, name = "account"),
    path('update-item/', views.userUpdateItemInCart, name= "update-item")
]