from django.shortcuts import render
from ae import emailcode
# Create your views here.
from django.shortcuts import render,redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Address, BillAddress,Order,Order_item
import re
from django.contrib.auth.decorators import login_required
from ae.models import product
# Create your views here.

def login(request):
    if request.method == 'POST' :
      email = request.POST['email']
      password = request.POST['password']

      user = auth.authenticate(username=email, password=password)
      
      if user is not None :
        auth.login(request, user)
        
        
        return redirect("/")

      else :
        messages.info(request,'invalid creds..')
        return redirect("/")

    else :    
      return render(request,'index.html')

def logout(request):
  auth.logout(request)
  return redirect("/")


def register(request):
    if request.method == 'POST' :
       first_name = request.POST['fname']
       last_name = request.POST['lname']
       username = request.POST['email']
       email = request.POST['email']
       pass1 = request.POST['pasword1']
       pass2 = request.POST['pasword2']
       
       if pass1 == pass2 :
          if User.objects.filter(email=email).exists():
              print("Email is already present")
              messages.info(request,'Email is already present')
              return redirect('register')
          else:
             user=User.objects.create_user(username=username, password=pass1, email=email,first_name=first_name, last_name=last_name)
             user.save()
             print('User Created Successfully')
             #toemail = email
             #msg_content='Dear User, \n Welcome to Alientronics.\n We are glad to have you onboard. \n  \n \n\n\n\n Best Regards, \n Alientronics Team'
             #sub='Welcome to Alientronics'
             #emailcode.sendEmail(toemail,sub,msg_content)
             return redirect('/')
             
       else :
           print("Passwords not matching")
           messages.info(request,'Passwords not matching')
           return redirect('register')
       
     

    else :    
     return render(request,'register.html')

def add_address(request) :
  if request.method == 'POST':
    address= request.POST['address']
    address2= request.POST['address2']
    area=request.POST['area']
    phone_number=request.POST['phone']
    district=request.POST['district']
    city=request.POST['City']
    State=request.POST['State']
    Pin_Code=request.POST['Pin_Code']
    #Name=request.POST['name']

    if isValid(phone_number):
         print("Phone number validated , proceeding with add address flow ")     
    
         try:
          bill=request.POST['bill']
          print(bill)
          add_billaddress(request)


         except:
           print("bill not checked")
           bill="Not checked"
    
         user = request.POST['user_id']
    

         print("Proceeding to write address details in database")

         addrr=Address.objects.filter(user_id = user,default=True ).exists()
         #billexist=BillAddress.objects.filter(user_id = user,default=True ).exists()
         if addrr :
           print("ship address exists ")
           messages.info(request,"Uh Ohh !!! default address is already there , try deleting the default address and try again")
           return redirect("/accounts/address")
    
         else :

            print("ship or bill address does not exists")
       
            #if not billexist:
             #    Bill = BillAddress.objects.create(Name=Name,address=address,address2=address2,area=area,phone_number=phone_number,district=district,State=State,City=city,Pin_Code=Pin_Code,default=True,user_id=user)
             #    Bill.save()
             #    print("billed address saved succesfully")
            #else:
             #  print("in bill bill not exist else paer")

       
            try :
                 addrssobj = Address.objects.create(address=address,address2=address2,area=area,phone_number=phone_number,district=district,State=State,City=city,Pin_Code=Pin_Code,default=True,user_id=user)
                 addrssobj.save()
                 print("Addresses saved successfully ... ")
                 #messages.info(request,"Address Added Successfully")
            except Exception as e  :
               print(" Exceptions occurred during database operation ...")
               print(e)
               messages.info(request,"Uh Ohh !!! There is some temporary error , please try again later / currently you can add only one addtess at a time")
       
         return redirect("/accounts/address")
    else:
       print("Phone number is not valid")
       messages.info(request,"Enter a valid phone number!!")
       
       return redirect("/accounts/address")
       

  else :
    
         return render(request,'address_add.html')



def address_view(request):

 if request.user.is_authenticated:
    user_id= request.user.id
    if request.method =='POST' :
      print('POST received')
  
    else :
      print("GET method received ")
      print("calling function")
      userobjj = Address.objects.filter(user_id = user_id).exists()
      billobj=BillAddress.objects.filter(user_id = user_id).exists()
      if userobjj and  billobj:
            print(" Reading from address and bill database table")
            addrobj= Address.objects.filter(user_id = user_id).values
            billaddrobj= BillAddress.objects.filter(user_id = user_id).values
            
            context = {
                  'address': addrobj,
                  'billaddress':billaddrobj
                  
                }
            #print(addrobj)
            return render(request,'address.html',context)
      elif billobj:
            print("no shipped data Reading from billed address database table")
            billaddrobj= BillAddress.objects.filter(user_id = user_id).values
            
            context = {
                  'billaddress': billaddrobj,
                  
                }
            print(billaddrobj)
            return render(request,'address.html',context)
      elif userobjj:
            print("no billed data Reading from address database table")
            addrobj= Address.objects.filter(user_id = user_id).values
            
            context = {
                  'address': addrobj,
                  
                }
            #print(billaddrobj)
            return render(request,'address.html',context)

      else :
        messages.info(request,'No saved Address')
        print(" No address")
        return render(request,'address.html')
      
      
      

 else :
     return redirect("/accounts/login")



def del_address(request) :
  if request.method == 'GET':
    if request.user.is_authenticated :
      user_id=request.user.id
      try : 

         Addressobj=Address.objects.get(user_id = user_id)
         print("Addressobj",Addressobj)
         Addressobj.delete()
         print("deleted ..")
         # return render(request,"address.html")

      except Exception as e :
       print(e)

    
      messages.info(request,"deleted")
      print("Deleted")
      return redirect("/accounts/address")

    else :
      return redirect("/")

  else :
    return redirect("/accounts/address")
    

def add_billaddress(request) :
  if request.method == 'POST':
    address= request.POST['address']
    address2= request.POST['address2']
    area=request.POST['area']
    phone_number=request.POST['phone']
    district=request.POST['district']
    city=request.POST['City']
    State=request.POST['State']
    Pin_Code=request.POST['Pin_Code']
    Name=request.POST['name']
    
    #try:
    #  bill=request.POST['bill']
    #  print(bill)

    #except:
    #  print("bill not checked")
    #  bill="Not checked"
    
    user = request.POST['user_id']
    

    print("Proceeding to write billed address details in database")

    addrr=BillAddress.objects.filter(user_id = user,default=True ).exists()
    #billexist=BillAddress.objects.filter(user_id = user,default=True ).exists()
    if addrr :
      print("Billed address exists ")
      messages.info(request,"Uh Ohh !!! default address is already there , try deleting the default address and try again")
      return redirect("/accounts/address")
    
    else :

       print("bill address does not exists")
       
       #if not billexist:
        #    Bill = BillAddress.objects.create(Name=Name,address=address,address2=address2,area=area,phone_number=phone_number,district=district,State=State,City=city,Pin_Code=Pin_Code,default=True,user_id=user)
        #    Bill.save()
        #    print("billed address saved succesfully")
       #else:
        #  print("in bill bill not exist else paer")

       
       try :
            billobj = BillAddress.objects.create(Name=Name,address=address,address2=address2,area=area,phone_number=phone_number,district=district,State=State,City=city,Pin_Code=Pin_Code,default=True,user_id=user)
            billobj.save()
            print("Billed Addresses saved successfully ... ")
            #messages.info(request,"Address Added Successfully")
       except Exception as e  :
          print(" Exceptions occurred during database operation ...")
          print(e)
          messages.info(request,"Uh Ohh !!! There is some temporary error , please try again later / currently you can add only one addtess at a time")
       
    return redirect("/accounts/address")


  else :
    
    return render(request,'address_add.html') 

def del_billaddress(request) :
  if request.method == 'GET':
    if request.user.is_authenticated :
      user_id=request.user.id
      try : 

         Addressobj=BillAddress.objects.get(user_id = user_id)
         print("Addressobj",Addressobj)
         Addressobj.delete()
         print("deleted billed adddress ..")
         # return render(request,"address.html")

      except Exception as e :
       print(e)

    
      messages.info(request,"deleted")
      print("Deleted")
      return redirect("/accounts/address")

    else :
      return redirect("/")

  else :
    return redirect("/accounts/address")
 

def order(request):
  if request.user.is_authenticated:

       user_id  = request.user.id 
       orderobj = Order.objects.filter(user_id=user_id).values
       print("order details Retrieved",orderobj)
       return render(request , 'orderdetails.html',{'order': orderobj})

  else:
        return redirect("/")

@login_required(login_url="/accounts/login")
def cancel_order(request):
  if request.method=='POST':
    order_id=request.POST['order_id']
    email=request.POST['email']
    print("Order ID received to cancel is --->",order_id)
    orderobj = Order.objects.get(id=order_id) 
    
   
    if orderobj.ORDER_STATUS == "SHIPPED":
        print("Order cannot be cancelled after shipping ")
        messages.error(request,"Order cannot be cancelled after shipping")
        return redirect("/accounts/order")
    else: 
         print("Starting to cancel order")
         try :
               orderobj.ORDER_STATUS ="CANCELLED"
               orderobj.save()
               print("Order has been cancelled successfully ")
               msg_content='Dear User, \n Your Order has been cancelled succesfully .\n We look forward to see you soon. \n  \n \n\n\n\n Best Regards, \n Alientronics Team'
               sub='Order Cancelled Successfully'
               toemail=email
               emailcode.sendEmail(toemail,sub,msg_content)
               value=Order_item.objects.filter(order_id=order_id)
               for i in value :
                 print("oRDER_STATUS",i.ORDER_STATUS)
                 orderitemobj=Order_item.objects.get(order_id=order_id)
                 orderitemobj.ORDER_STATUS="CANCELLED"
                 can_qty=orderitemobj.item_qty
                 product_id1=orderitemobj.product_id
                 orderitemobj.save()
                 Productobj=product.objects.get(id=product_id1)
                 curr_invt=Productobj.inventory
                 updated_invt=curr_invt+can_qty
                 print("Current inventory is ",curr_invt,"for product name -",Productobj.name,"to be updated to-",updated_invt)
                 
                 #print("Latest inventory is ",updated_invt)
                 Productobj.inventory=updated_invt
                 Productobj.save()
               print("Order items cancelled successfully ") 
               return redirect("/accounts/order")  
         except Exception as e :
           print("Exception while cancelling order")
           print(e)
           return redirect("/accounts/order")
  else :
    return redirect("/accounts/order")

def isValid(s):
     
    # 1) Begins with 0 or 91
    # 2) Then contains 6,7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)
 


"""""
def orders(request):
  if request.user.is_authenticated :
      user_id = request.user.id
      print('Reading past order details from database')
      try :
         items = Order_item.objects.filter(user_id = user_id).values
         print('items returned from db are  -- > ', items)
         context = {
             'items': items,
           }

      except  :
        
        
        print('No items returned')
      return render(request,'orders.html',context)

  else :
    messages.info(request,'User must login ')
    return render(request,'orders.html')


def address_view(request):

 if request.user.is_authenticated:
    user_id= request.user.id
    if request.method =='POST' :
      print('POST received')
  
    else :
      print("GET method received ")
      print("calling function")
      userobjj = Address.objects.filter(user_id = user_id).exists()
      if userobjj :
            print(" Reading from address database table")
            addrobj= Address.objects.filter(user_id = user_id).values
            context = {
                  'address': addrobj
                }
            print(addrobj)
            return render(request,'address.html',context)

      else :
        messages.info(request,'No saved Address')
        print(" No address")
        return render(request,'address.html')
      
      
      

 else :
     return redirect("/accounts/login")



def add_address(request) :
  if request.method == 'POST':
    address= request.POST['Address']
    address2= request.POST['Address2']
    area=request.POST['area']
    phone_number=request.POST['phone_number']
    district=request.POST['district']
    State=request.POST['State']
    Pin_Code=request.POST['Pin_Code']
    default = request.POST['default']
    user = request.POST['user_id']

    print("Proceeding to write address details in database")

    addrr=Address.objects.filter(user_id = user,default=True ).exists()
    if addrr :
      print("Default address exists ")
      messages.info(request,"Uh Ohh !!! default address is already there , try deleting the default address and try again")
      return redirect("/accounts/add_address")


    else :

       print("default does not exists")

       try :
            addrssobj = Address.objects.create(address=address,address2=address2,area=area,phone_number=phone_number,district=district,State=State,Pin_Code=Pin_Code,default=default,user_id=user)
            addrssobj.save()
            print("Addresses saved successfully ... ")
            messages.info(request,"Address Added Successfully")
       except Exception as e  :
          print(" Exceptions occurred during database operation ...")
          print(e)
          messages.info(request,"Uh Ohh !!! There is some temporary error , please try again later / currently you can add only one addtess at a time")

    return redirect("/accounts/address")



  else :
   return render(request,'add_address.html') 
  

def del_address(request) :
  if request.method == 'GET':
    if request.user.is_authenticated :
      user_id=request.user.id
      try : 


         Addressobj=Address.objects.get(user_id = user_id)
         print("Addressobj",Addressobj)
         Addressobj.delete()
         print("deleted ..")
         # return render(request,"address.html")

      except Exception as e :
       print(e)

    
      messages.info(request,"deleted")
      return redirect("/accounts/address")

    else :
      return redirect("/accounts/login")

  else :
    return redirect("/accounts/address")
    

  
  
      




def account(request):
  user_id= request.user.id
  addrobj1= Address.objects.filter(user_id = user_id).values
  context = {
                  'address': addrobj1
                }

  return render(request,"account.html",context)


def add_offline_customer(request):
  if request.method == 'POST':
     created_by=request.POST['Associate_name']
     associate_email=request.POST['Associate_email']
     customer_name=request.POST['customer_name']
     customer_Phone_number=request.POST['phone_number']
     customer_email=request.POST['email']
     address1=request.POST['Address']
     address2=request.POST['Address2']
     State=request.POST['State']
     City=request.POST['City']
     District=request.POST['district']
     Pin_Code=request.POST['Pin_Code']

     print("Starting with db connection for saving offline customer")

     try:
         
         
         
         obj=offline_customer.objects.create(created_by=created_by,associate_email=associate_email,customer_name=customer_name,customer_Phone_number=customer_Phone_number,customer_email=customer_email,address1=address1,address2=address2,State=State,
         City=City,District=District,Pin_Code=Pin_Code)
         obj.save()
         print("Details saved to db successfully")
         messages.info(request,"Details saved successfully")

     except Exception as e:
         print("***************")
         print(e)
         messages.info(request,"Some exceptions occurred")

     return redirect("/accounts/view-offline-customer")

  else :
    # if reuest is a get method

       if request.user.is_authenticated :
         user_id=request.user.id
         associateid=Associate.objects.filter(user_id = user_id).exists()
         print(associateid)
         if associateid :
            print("Associate exists")
            return render(request,'offline_customer.html')

         else :
            print("User is not an associate")
            return redirect("/")

       else :
          print("Not logged in ...")
          return redirect("/accounts/login")


         

def view_offline_customer(request):
   if request.user.is_authenticated:
    user_email= request.user.email
    if request.method =='POST' :
      print('POST received')
  
    else :
      print("GET method received ")
      print("calling function")
      userobjj = offline_customer.objects.filter(associate_email = user_email).exists()
      if userobjj :
            print(" Reading from address database table")
            off_cust_obj= offline_customer.objects.filter(associate_email = user_email).values
            context = {
                  'off_cust_obj': off_cust_obj
                }
            print(off_cust_obj)
            return render(request,'view_added_customer.html',context)

      else :
        messages.info(request,'No saved customers')
        print(" No added customers")
        return render(request,'view_added_customer.html')


def view_offline_order(request):

  if request.user.is_authenticated :
      user_id = request.user.id
      print('Reading past order details from database')
      try :

         #search in associates table with the given userid 
         #search in offline order db with the associate names and get the values
         #pass all the values in frontend

         items = Order_item.objects.filter(user_id = user_id).values
         print('items returned from db are  -- > ', items)
         context = {
             'items': items,
           }

      except  :
        
        
        print('No items returned')
      return render(request,'orders.html',context)

  else :
    messages.info(request,'User must login ')
    return render(request,'orders.html')

      

"""


  
