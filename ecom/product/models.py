from collections.abc import Collection, Iterable
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
import uuid

class ActiveQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)
    

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()

    class MPTTMeta:
        order_insertion_by = ["parent"]

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()

    def __str__(self):
        return self.name
    
class Product_type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    objects=ActiveQuerySet().as_manager()
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["parent"]

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug=models.SlugField(max_length=200)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    product_type=models.ForeignKey(Product_type,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()
    def __str__(self):
        return self.name
    


class Productline(models.Model):
    price=models.DecimalField( max_digits=5, decimal_places=2)
    sku=models.CharField(max_length=30)
    stock_quantity=models.IntegerField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_line")
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()

    def __str__(self):
        return str(self.sku)
    

class Product_image(models.Model):
    name = models.CharField(max_length=100)
    alternative_text=models.CharField(max_length=100)
    productline=models.ForeignKey(Productline,on_delete=models.CASCADE,related_name="product_image")

    def save(self,*args,**kwargs):
        self.full_clean()
        return super(Product_image,self).save(*args,**kwargs)
    def __str__(self):
        return str(self.name)