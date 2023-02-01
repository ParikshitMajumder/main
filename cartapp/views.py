
from django.shortcuts import render, redirect
from ae.models import product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages


# Create your views here.
@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    
    cart.add(product=Product)
    return redirect("/cart/cart-detail/")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    cart.remove(Product)
    return redirect("/cart/cart-detail/")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    id=id
    cart = Cart(request)
    Product = product.objects.get(id=id)
    qty=Product.inventory
    print("Current product inventory is -",qty)
    value = request.session['cart']
    for i in value : 
        order_item = value[i]
        
        prod_id=order_item['product_id']
        
        if id == prod_id :
            cart_qty=order_item['quantity']
            print("Cart qty =",cart_qty)
            #request.session['cart'][i]['quantity']=1

    if cart_qty < qty :
        cart.add(product=Product)
        return redirect("/cart/cart-detail/")
    else :
        print("Item quantity is expedited")
        messages.warning(request,"more quantity is not available for the product")
        return redirect("/cart/cart-detail/")

    
    
    


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    cart.decrement(product=Product)
    return redirect("/cart/cart-detail/")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/")


@login_required(login_url="/accounts/login")
def cart_clear_auto(request):
    cart = Cart(request)
    cart.clear()
    
    return render(request,'success.html')


@login_required(login_url="/accounts/login")
def cart_detail(request):
   #Product= product.objects.all()
   #associate=Associate.objects.all()
   

   return render(request,'cart-detail.html')
   

