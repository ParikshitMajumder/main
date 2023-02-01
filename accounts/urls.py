from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('address', views.address_view, name="address"),
    path('address/add', views.add_address, name="add_address"),
    path('address/delete', views.del_address, name="del_address"),
    path('address/bill/add', views.add_billaddress, name="add_billaddress"),
    path('address/bill/delete', views.del_billaddress, name="del_billaddress"),
    path('order', views.order, name="order"),
    path('order/cancel', views.cancel_order, name="cancel_order"),
]