from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from ae.models import product , Cartdb , CartItem
from accounts.models import *
import random
import string
from cartapp.views import cart_clear
from django.contrib import messages
from ae import emailcode

# Create your views here.

def checkout(request):
    if request.user.is_authenticated:
     if request.method == 'POST':
        amount=request.POST['amount']
        amount1=int(float(amount))
        #method=request.POST['paymentMethod']
        #we will save details in cart db 
        print("Starting cart db operation ..")
        save_cart(request,amount1)
 
        #print("POST recieved")
        return render(request,'checkout.html')
       
     else:
        return render(request,'checkout.html')

    else:

        return redirect("/")



def save_cart(request,amt):
    # checking login 
     qty =0
     cart_item_dict={}
     To_delete = False
     
     
     save = False
     if request.user.is_authenticated:
         
         amount = amt
         userid=request.user.id
         value=request.session['cart']
         #cart_item=value['3']
         print('user_id through session' ,userid)
         #print('user_id through cart' ,cart_item)
         #print('cart user id ',cart_item['userid'])
         #print('Amount received ' ,amount )
         # using try catch block to avoid index out of bound , if out of bound then user is not present.
         try :
              cart_userid=Cartdb.objects.filter(user_id = userid).values_list('user_id', flat=True)[0]
              print('from cart db ',cart_userid)
              

         except :
            print('no user data present in db ')
            cart_userid = 0
            
         
         print(len(value))
         print(value)
         #looping thorugh dictionary
         for i in value:    # taking each cart id 
             cart_item = value[i]
             cart_item_dict[i]={}
             userid1 = cart_item['userid']
             product_id = cart_item['product_id']
             product_name = cart_item['name']
             product_price =cart_item['price']
             product_price1=int(float(product_price))
             item_qty = cart_item['quantity']
             

             if userid == cart_userid :      # need to check whether cart is present in db then save or update 
                qty= qty + cart_item['quantity']
                
                cart_item_dict[i]['userid']=userid1
                cart_item_dict[i]['product_id']=product_id
                cart_item_dict[i]['name']=product_name
                cart_item_dict[i]['quantity']=item_qty
                cart_item_dict[i]['price']=product_price
                



                save = False
                To_delete = True
                
                

                #cart_id=Cartdb.objects.filter(user_id = userid).values_list('id', flat=True)[0]
                #cartitemobj = CartItem.objects.get(user_id = userid)
               # cartitemobj.product_id=product_id
                #cartitemobj.product_name=product_name
                #cartitemobj.price = product_price1
                #cartitemobj.quantity =item_qty
                #cartitemobj.cartdb_id=cart_id
                #cartitemobj.save()

             else :
                qty= qty + cart_item['quantity']
                cart_item_dict[i]['userid']=userid1
                cart_item_dict[i]['product_id']=product_id
                cart_item_dict[i]['name']=product_name
                cart_item_dict[i]['quantity']=item_qty
                cart_item_dict[i]['price']=product_price
                
                save = True
               
                
                
             #print('inside for loop' ,cart_item)
             #print(value[i])

         print('Total quantity - ', qty)
         if To_delete :
            cartobj1=Cartdb.objects.get(user_id = userid)
            #cartobj1.Total_amount = amount
            # deleting the existing cart item
            cartobj1.delete()
            print('update operation -->Previous cart deleted for the user ')
         else :
            print('Creating new cart for the user as no cart was previously present in db ')
            print('save operation -->This is a save operation as no cart found for user')


         if save :
             print('startingdatabase save operation ..')
                
             cartobj=Cartdb.objects.create(user_id=userid1, Total_amount=amount,total_quantity=qty)
             cartobj.save()
             #cart_id=Cartdb.objects.filter(user_id = userid).values_list('id', flat=True)[0]
             #cartitemobj= CartItem.objects.create(user_id=userid1 ,product_id =product_id,product_name=product_name, price = product_price1,quantity =item_qty,cartdb_id=cart_id)
             #cartitemobj.save()
             # getting cart id using user id 
             print('cart saved , starting to save cart item obj for userid ->',userid)

             cartid=Cartdb.objects.filter(user_id = userid).values_list('id', flat=True)[0]
             print('cart item reeceived from session is ', cart_item_dict)
             for j in cart_item_dict :
                item = cart_item_dict[j]
                userid1=item['userid']
                product_id=item['product_id']
                product_name=item['name']
                item_qty=item['quantity']
                product_price=item['price']
                price=int(float(product_price))
               
                cartitemobj=CartItem.objects.create(user_id=userid1,product_id=product_id,product_name=product_name,quantity=item_qty,price=price,cart_id = cartid )
                cartitemobj.save()


            
             print('database save operation completed.., --> proceeding to create order from server for payment gateway')

         else :
            
            
            # saving the cart item
            print('update operation --> starting database update operaton ')
            cartobj=Cartdb.objects.create(user_id=userid1, Total_amount=amount,total_quantity=qty)
            cartobj.save()
            print('cart saved , ---> starting to save cart item in database , at this stahe if circuit breaks need to manually delete the cart for userid ',userid)
            cartid=Cartdb.objects.filter(user_id = userid).values_list('id', flat=True)[0]
            for j in cart_item_dict :
                item = cart_item_dict[j]
                userid1=item['userid']
                product_id=item['product_id']
                product_name=item['name']
                item_qty=item['quantity']
                product_price=item['price']
                price=int(float(product_price))
               
                cartitemobj=CartItem.objects.create(user_id=userid1,product_id=product_id,product_name=product_name,quantity=item_qty,price=price,cart_id = cartid )
                cartitemobj.save()
           
            
            print('database update operation completed successfully , --> proceeding to create order from server for payment gatewway')
    
    #print (userid['name'])


def payhandler(request):
    if request.method == 'POST':
       method=request.POST['paymentMethod']
       email=request.POST['email']
       value = request.session['cart']
       
       for i in value : 
          order_item = value[i]
        
          prod_id=order_item['product_id']
          cart_qty=order_item['quantity']
          Product = product.objects.get(id=prod_id)
          qty=Product.inventory
          print("Cart quantity is - ",cart_qty,"DB quantity is --",qty)
          print(type(cart_qty),"db type",type(qty))
          if cart_qty <= qty :
             check=True
          else:
             check=False
             break
       print(check)
       if check : 
             if method == "online":
               print("Online ")
             else: 
               print(method)
               print("Calling cod order function")
               try:
                  cod_order(request)  
                  msg_content='Dear User, \n Your Order has been placed succesfully with us.\n We will further update you once the item gets shipped. \n  \n \n\n\n\n Best Regards, \n Alientronics Team'
                  sub='Order Placed Successfully'
                  toemail=email
                  emailcode.sendEmail(toemail,sub,msg_content)
               except Exception as e:
                    print(e)
               print("Clearing cart")
               cart_clear(request)
               return redirect("/payment/success")
       else:
              print("Item has been expedited")
              return redirect("/cart/cart_clear")

    return redirect("/payment/checkout")


def cod_order(request):
    name= request.user.first_name 
    provider_order_id=ran_gen(8, "AEIOSUMA23")
    payment_id=ran_gen(8, "AEIOSUMA23")
    signature_id = ran_gen(8, "AEIOSUMA23")
    user_id  = request.user.id 
    isPaid = False
    cartamount=Cartdb.objects.filter(user_id = user_id).values_list('Total_amount', flat=True)[0]
    order_amount = cartamount
    mode="OFFLINE"
    ORDER_STATUS = "CREATED"

    orderobj=Order.objects.create(user_name=name , amount = order_amount , provider_order_id = provider_order_id ,payment_id=payment_id,signature_id=signature_id,user_id=user_id,isPaid=isPaid,mode=mode,ORDER_STATUS=ORDER_STATUS )
    orderobj.save()
    print('Order details saved to Database')
    print("calling function")
    orderdb_id=Order.objects.filter(user_id = user_id).values_list('id').latest('id')[0]
    print("Latest order id is ---------",orderdb_id)

    save_order(request ,provider_order_id,orderdb_id )
    print('Orderitems details saved to Database')


def save_order (request,provider_id,orderdb_id):
    order_dict = {}
    order_id = provider_id
    orderdb_id=orderdb_id
    
    if request.user.is_authenticated:
       
       value=request.session['cart']
       for i in value :
        order_item = value[i]
        order_dict[i]={}
        
        userid1 = order_item['userid']
        product_id = order_item['product_id']
        product_name = order_item['name']
        product_price =order_item['price']
        product_price1=int(float(product_price))
        item_qty = order_item['quantity']
        ORDER_STATUS="CREATED"
        #image=order_item['image']
        product_id1=product.objects.filter(id=product_id).values_list('id', flat=True)[0]
        print('product_id -',product_id1)
        Productobj=product.objects.get(id=product_id1)
        curr_invt=Productobj.inventory
        print("Current inventory is ",curr_invt,"Type ",type(curr_invt))
        updated_invt=curr_invt-item_qty
        print("Latest inventory is ",updated_invt)
        Productobj.inventory=updated_invt
        Productobj.save()
        order_itemobj = Order_item.objects.create(user_id =userid1,product_id=product_id1 ,product_name=product_name,product_price = product_price1,provider_order_id= order_id,item_qty=item_qty,ORDER_STATUS=ORDER_STATUS,order_id=orderdb_id)
        order_itemobj.save()
   
        print('Ordred items saved successfully ...')

def success(request):

    if request.user.is_authenticated:

       #user_id  = request.user.id 
       #orderobj = Order.objects.filter(user_id=user_id).values
       #print("order details ",orderobj)
       messages.success(request,"Order has been placed successfully")
       return redirect("/accounts/order")
       return render(request , 'success.html',{'order': orderobj})

    else:
        return redirect("/")


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
 
# function call for random string
# generation with size 8 and string
#print (ran_gen(8, "AEIOSUMA23"))