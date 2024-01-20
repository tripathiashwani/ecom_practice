from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.serializers import BrandSerializer,productLineSerializer,productSerializer,categorySerializer
from .models import Category,Brand,Product
from drf_spectacular.utils import extend_schema
# Create your views here.

class brandViewSet(viewsets.ViewSet):
    queryset=Brand.objects.all()
    @extend_schema(responses=BrandSerializer)
    def list(self,request):
        serializer=BrandSerializer(self.queryset,many=True)
        return Response(serializer.data)
    

class productViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing all products
    """
    queryset=Product.objects.all()
    lookup_field="slug"
    def retrieve(self,request,slug=None):
        """A viewset for view product by id """
        serializer=productSerializer(self.queryset.filter(slug=slug).select_related("category","brand")
        .prefetch_related("product_line").prefetch_related("product_line__product_image")
        ,many=True)
        return Response(serializer.data)
    

    @extend_schema(responses=productSerializer)
    def list(self,request):
        serializer=productSerializer(self.queryset,many=True)
        return Response(serializer.data)
    

class CategoryViewSet(viewsets.ViewSet):
    

    queryset=Category.objects.all()
    lookup_field="slug"
    def retrieve(self,request,slug=None):
        """A viewset for view product by category """
        serializer=categorySerializer(self.queryset.filter(slug=slug)
        .prefetch_related("product")
        ,many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=categorySerializer)
    def list(self,request):
        serializer=categorySerializer(self.queryset,many=True)
        return Response(serializer.data)