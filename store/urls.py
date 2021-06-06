from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = "store"),
    path('search/', views.search, name = "search"),
    path('sortPrice/', views.sortPrice, name = "sortPrice"),
    path('category/<slug:category>/', views.category, name = "category"),
    path('cart/', views.cart, name = "cart"),
    path('checkout/', views.checkout, name = "checkout"),
    path('account/', views.account, name = "account"),
    path('update-item/', views.userUpdateItemInCart, name= "update-item"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('process_payment/', views.processedPayment, name= "process_payment"),
    path('successful/<pk>', views.successfulPayment, name='success'),
    # path('invoice/', views.showInvoice, name='invoice'),
    path('profile/', views.profile, name="profile"),
    path('add-comment/', views.addComment, name="add-comment"),
    path('add-rating/', views.addRating, name="add-rating"),
    path('refund/<int:id>/', views.refund, name='refund'),
    path('refund-detail/<int:id>/', views.refundDetail, name='refund-detail'),
    
]