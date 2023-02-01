from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(product_category)
admin.site.register(product_inventory)
admin.site.register(discount)
admin.site.register(invoice)
admin.site.register(product)
admin.site.register(bullet_point)
admin.site.register(images)
admin.site.register(Cartdb)
admin.site.register(CartItem)
