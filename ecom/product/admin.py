# your_app/admin.py

from django.contrib import admin
from .models import Brand,Product,Productline,Product_image,Category,Product_type

admin.site.register(Brand)
admin.site.register(Product_image)
admin.site.register(Productline)
admin.site.register(Product)
admin.site.register(Product_type)
admin.site.register(Category)

