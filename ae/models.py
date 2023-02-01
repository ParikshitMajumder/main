from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime
import uuid
import random , string


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# Create your models here.

class BaseModel(models.Model):
    #id= models.CharField(primary_key=True,editable=False,default=ran_gen(4, "AEMA23673"),max_length=5)
    #uid= models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4())
    created_at= models.DateTimeField(default=datetime.now)
    #created_at= models.DateField(default=datetime.now)

    class Meta:
        abstract=True

# 1st level models
class product_category(BaseModel):
    name=models.CharField(max_length=60)
    desc=models.TextField()
    modified_at=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.name} {self.id}"
    

class product_inventory(BaseModel):
    quantity=models.IntegerField()
    modified_at=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.quantity}"
    

class discount(BaseModel):
    name=models.CharField(max_length=60)
    desc=models.TextField()
    discount_percent=models.FloatField()
    modified_at=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.name}"
    

class invoice(models.Model):
    number=models.CharField(max_length=60)
    desc=models.TextField()
    shop=models.CharField(max_length=200)
    date=models.DateTimeField(default=datetime.now)
    modified_at=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.shop} number- {self.number}"
    

#2nd level models

"""class product(BaseModel):
    name=models.CharField(max_length=200)
    desc=models.TextField()
    HSN_SAC=models.CharField(max_length=150)
    category_id=models.ForeignKey(product_category,on_delete=models.CASCADE)  
    inventory_id=models.ForeignKey(product_inventory,on_delete=models.CASCADE) 
    price=models.FloatField()
    MRP=models.FloatField()
    is_curated=models.BooleanField(default=False)
    discount_id=models.ForeignKey(discount,on_delete=models.CASCADE)
    modified_at=models.DateTimeField(default=datetime.now)
    #deleted_at=models.DateTimeField(default=datetime.now)

"""

class product(BaseModel):
    name=models.CharField(max_length=200)
    desc=models.TextField()
    HSN_SAC=models.CharField(max_length=150)
    category_id=models.ForeignKey(product_category,on_delete=models.CASCADE)  
    inventory=models.IntegerField()
    price=models.FloatField()
    MRP=models.FloatField()
    is_curated=models.BooleanField(default=False)
    invoice=models.ForeignKey(invoice, on_delete=models.CASCADE)
    discount_id=models.ForeignKey(discount,on_delete=models.CASCADE)
    modified_at=models.DateTimeField(default=datetime.now)
    main_image=models.ImageField(upload_to='pics')
    #deleted_at=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} id {self.id}"


class bullet_point(models.Model):
    
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    point=models.CharField(max_length=60)
    modified_at=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.id} number- {self.product}"


class images(models.Model):
    url=models.ImageField(upload_to='pics')
    product=models.ForeignKey(product,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product}"


class Cartdb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Total_amount = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
   
    #cart_item_id = models.ForeignKey('CartItem', on_delete=models.CASCADE)
    total_quantity = models.IntegerField()
    #cartitem = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} amount {self.Total_amount}"

class CartItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    product_name=models.CharField(max_length=100)
    cart = models.ForeignKey(Cartdb,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} amount {self.product_name}"