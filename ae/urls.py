from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('',views.index, name="index"),
    path('about',views.about, name="about"),
    path('single',views.single, name="single"),
    path('software',views.software, name="software"),
    path('hardware',views.hardware, name="hardware"),
    path('contact',views.contact, name="contact"),
]