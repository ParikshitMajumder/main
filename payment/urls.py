from django.urls import path
from . import views

urlpatterns = [

    path('checkout',views.checkout,name="checkout"),
    path('checkout/handler',views.payhandler,name="payhandler"),
    path('success',views.success,name="success")

]