from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Address(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    address2 = models.TextField()
    area = models.TextField()
    district = models.TextField()
    City = models.TextField()
    State = models.TextField()
    Pin_Code = models.IntegerField()
    default = models.BooleanField(default=False)
    last_update=models.DateTimeField(default=datetime.now)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.user} pincode- {self.Pin_Code} District- {self.district}"



class Order(models.Model):
    #name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    user_name=models.CharField(max_length=100)
    amount = models.FloatField(null=False, blank=False)
    isPaid =models.BooleanField(default=False)
    provider_order_id = models.CharField(max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(max_length=128, null=False, blank=False
    )
    #product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #quantity = models.IntegerField(default=1)
    
    #product_name=models.CharField(max_length=100)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    ONLINE='Online'
    OFFLINE='Offline'
    ASSISTED='ASSISTED'
    order_choices = [
        (ONLINE, 'ONLINE'),
        (OFFLINE, 'OFFLINE'),
        (ASSISTED, 'ASSISTED'),
        
    ]
    mode=models.CharField(max_length=10,choices = order_choices,default=ASSISTED)
    IN_PROGRESS='IN_PROGRESS'
    CANCELLED='CANCELLED'
    SHIPPED='SHIPPED'
    ACCEPTED='ACCEPTED'
    NOT_CREATED='NOT_CREATED'
    CREATED='CREATED'
    order_status_choices = [
        (IN_PROGRESS, 'IN_PROGRESS'),
        (CANCELLED, 'CANCELLED'),
        (SHIPPED, 'SHIPPED'),
        (ACCEPTED, 'ACCEPTED'),
        (NOT_CREATED, 'NOT_CREATED'),
        (CREATED,'CREATED')
        
    ]
    ORDER_STATUS=models.CharField(max_length=15,choices = order_status_choices,default=NOT_CREATED)

    def __str__(self):
       return f"Placed By -{self.user_name}-Amount RS- {self.amount} /-- Mode-{self.mode}- Status --{self.ORDER_STATUS}"




class Order_item(models.Model):
 
        user_id = models.IntegerField()
        
        product_id = models.IntegerField()    
        
        product_name = models.CharField(max_length=100)
        product_price =models.FloatField()
        provider_order_id = models.CharField(max_length=40, null=False, blank=False)
        order_id=models.IntegerField(default=1)
        item_qty = models.IntegerField()
        #image=models.ImageField()
        created_at = models.DateTimeField(default=datetime.now)
        IN_PROGRESS='IN_PROGRESS'
        CANCELLED='CANCELLED'
        SHIPPED='SHIPPED'
        ACCEPTED='ACCEPTED'
        NOT_CREATED='NOT_CREATED'
        CREATED='CREATED'
        order_status_choices = [
        (IN_PROGRESS, 'IN_PROGRESS'),
        (CANCELLED, 'CANCELLED'),
        (SHIPPED, 'SHIPPED'),
        (ACCEPTED, 'ACCEPTED'),
        (NOT_CREATED, 'NOT_CREATED'),
        (CREATED,'CREATED')
        
         ]
        ORDER_STATUS=models.CharField(max_length=15,choices = order_status_choices,default=NOT_CREATED)

        def __str__(self):
            return f"Product name {self.product_name}-Order ID - {self.provider_order_id}- Created {self.created_at} - STATUS - {self.ORDER_STATUS}"


class BillAddress(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    address = models.TextField()
    address2 = models.TextField()
    area = models.TextField()
    district = models.TextField()
    City = models.TextField()
    State = models.TextField()
    Pin_Code = models.IntegerField()
    default = models.BooleanField(default=False)
    last_update=models.DateTimeField(default=datetime.now)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.user} pincode- {self.Pin_Code} District- {self.district}"

