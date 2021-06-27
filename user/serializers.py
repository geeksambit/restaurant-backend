from rest_framework import serializers
from .models import *
from rest_framework import exceptions

class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model =  User
        # fields = [
        # "name" ,
        # "email",     
        # "mobile_no",
        # "password",
        # "created_date",
        # "updated_date",
        # "social_id",
        # "address"
        # ]
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
   class Meta:
        model =  User
        fields = [
        "id",
        "name" ,
        "email",     
        "mobile_no",
        "created_date",
        "updated_date",
        "social_id"
        ]
        # fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
   class Meta:
        model = ShippingAdress
       
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
   class Meta:
        model = Vendor
       
        fields = '__all__'

class VendorLoginSerializer(serializers.ModelSerializer):
   class Meta:
        model = Vendor
       
        fields = [
                "id",
                "name",
                "email",
                "mobile_no",
                # "password",
                "created_date",
                "address",
                "longitude",
                "latitude",
                "image"
        ]

class DeliveryBoySerializer(serializers.ModelSerializer):
   class Meta:
        model = DeliveryBoy
       
        fields = '__all__'
  
   
