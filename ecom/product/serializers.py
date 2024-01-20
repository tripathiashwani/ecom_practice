from rest_framework import serializers
from product.models import Brand,Category,Product,Product_image,Productline,Product_type,ProductLineAttributeValue,Attribute,AttributeValue,ProductTypeAttribute

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'


class productLineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Productline
        fields='__all__'

class productSerializer(serializers.ModelSerializer):
    brand_name=serializers.CharField(source="brand.name")
    category_name=serializers.CharField(source="category.name")
    product_line=productLineSerializer(many=True)
    class Meta:
        model=Product
        fields=["name","slug","description","brand_name","category_name","product_line"]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "slug", "is_active"]

class categorySerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer(many=True)
    class Meta:
        model=Category
        fields=["name","slug","product"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product_image
        fields='__all__'


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product_type
        fields='__all__'

class ProductLineAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductLineAttributeValue
        fields='__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attribute
        fields='__all__'

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model=AttributeValue
        fields='__all__'


class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductTypeAttribute
        fields='__all__'

