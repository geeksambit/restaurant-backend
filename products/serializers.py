from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import *
from rest_framework import exceptions



class CategorySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Category
        
        fields = '__all__'

class CuisineSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        
        fields = '__all__'

class ProductSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        
        fields = '__all__'

class ProductByCuisineSerialzer(serializers.ModelSerializer):
    #product_name = serializers.CharField()
    #image = serializers.CharField()
    product = ProductSerialzer(many=True)
    class Meta:
        model = Cuisine
        #fields = '__all__'
        
        fields = [

            "id",
            "cuisine_name",
            "image",
            "is_active",
            "product"
        ]

class AllProductsByCategorySerilizer(serializers.ModelSerializer):

    product = ProductSerialzer(many=True)
    class Meta:

        model = Category
        #fields = '__all__'
        
        fields = [

            "id",
            "category_name",
            "image",
            "is_active",
            "product"
        ]