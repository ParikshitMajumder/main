from django.shortcuts import render
from .models import product, images,bullet_point

# Create your views here.

def index(request):
    Product = product.objects.all()
    image= images.objects.all()
    return render(request,'index.html',{'products':Product,'image':image})

def about(request):
    return render(request,'about.html')

def single(request):
    if request.method == 'GET':
        id=request.GET.get('id')
        print("Received id ", id)
        Product = product.objects.filter(id=id).values()
        imagess=images.objects.filter(product=id).values()
        points= bullet_point.objects.filter(product=id).values()

        #print(type(Product.name))
        

        return render(request,'single.html',{'product':Product, 'extra':imagess,'points':points})

def software(request):
    Product = product.objects.filter(category_id=2).values()
    
    return render(request,'shopsoftware.html',{'products':Product})

def hardware(request):
    Product = product.objects.all().exclude(category_id=2)
    
    return render(request,'shophardware.html',{'products':Product})

def contact(request):
    return render(request,'contactus.html')