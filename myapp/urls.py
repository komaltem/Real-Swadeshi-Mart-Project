"""martproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from .views import Cart, index, check_out, Orders, Login, Signup, SelSignup, SellerSignin, cureview, user_dashboard

urlpatterns = [
    path('', index.as_view(), name="index"),
    path('BecomeSeller', views.BecomeSeller, name="BecomeSeller"),
    path('SellerSignin', SellerSignin.as_view(), name="SellerSignin"),
    path('sellregistration', SelSignup.as_view(), name="sellregistration"),
    path('seller_dashboard', views.seller_dashboard, name="seller_dashboard"),
    path('product_upload', views.product_upload, name="product_upload"),
    path('sellogout', views.sellogout, name="sellogout"),

    path('custlocation', views.custlocation, name="custlocation"),
    path('sign_up',Signup.as_view(), name="sign_up"),
    path('login', Login.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('user_dashboard', user_dashboard.as_view(), name="user_dashboard"),
    path('cart', Cart.as_view(), name="cart"),
    path('check_out', check_out.as_view(), name="check_out"),
    path('orders', Orders.as_view(), name="orders"),
    path('edit_cust', views.edit_cust, name="edit_cust"),
    path('wecome', views.wecome, name="wecome"),
    path('reviews', views.reviews, name="reviews"),
    path('cureview', cureview.as_view(), name="cureview"),
    path('search', views.search, name='search'),

]
