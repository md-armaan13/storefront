"""
URL configuration for strorefront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('collections/', views.CollectionList.as_view(), name='collectio_list'),
   # path('product/create/', views.ProductList.as_view(), name='product_create'),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection_detail'),
    path('products/<int:pk>/reviews/', views.ReviewList.as_view(), name='review_list'),
    path('products/<int:pk>/reviews/<int:review_pk>/', views.ReviewDetail.as_view(), name='review_detail'),
    path('products/<int:pk>/review/', views.review_create, name='review_list_sample'),
    path('carts/', views.CartList.as_view(), name='cart_create'),
    path('carts/<uuid:pk>/', views.CartDetail.as_view(), name='cart_detail'),
    path('carts/<uuid:pk>/items/', views.CartItemList.as_view(), name='cart_item_list'),
    path('carts/<uuid:cart_pk>/items/<int:pk>/', views.CartItemDetail.as_view(), name='cart_item_detail'),

    path('customers/', views.CustomerList.as_view(), name='Current_user_list'),
    path('customers/me/', views.CustomerDetail.as_view(), name='Current_user_detail'),

    path('orders/', views.OrderList.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),

    path('products/<int:product_pk>/images/', views.ProductImageList.as_view(), name='product_image_list'),

]   

#how to add UUID params in query url
