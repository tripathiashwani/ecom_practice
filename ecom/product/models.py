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
    slug = models.SlugField(max_length=255)
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
    
class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )
    def __str__(self):
        return f"{self.attribute.name}-{self.attribute_value}"
    

class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product_line = models.ForeignKey(
        "ProductLine",
        on_delete=models.CASCADE,
        related_name="product_attribute_value_pl",
    )


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        "Product_type",
        on_delete=models.CASCADE,
        related_name="product_type_attribute_pt",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_at",
    )


class Product_type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    attribute = models.ManyToManyField(
        Attribute,
        through="ProductTypeAttribute",
        related_name="product_Type_attribute",
    )
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug=models.SlugField(max_length=200)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True,related_name="product"
    )
    product_type=models.ForeignKey(Product_type,null=True,on_delete=models.CASCADE)
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
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )
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