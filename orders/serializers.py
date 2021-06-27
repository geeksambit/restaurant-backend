from rest_framework import serializers
from orders.models import *
from products.models import *


class CartSerialzer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(required=False)

    class Meta:
        model = Cart
        
        fields = [
            "id",
            "order_id",
            "product",
            "quantity",
            "ammount",
            "is_ordered",
            # "order_status",
            "created_date"

        ]
        depth = 1


class OrderSerialzer(serializers.ModelSerializer):

    cart = CartSerialzer(many =True)
    class Meta:
        model = Order
        
        fields = [
            "id",

            # "user" ,
            "order_id", 
            "order_status",
            "ammount",
            "address", 
            "is_paid", 
            "payment_details",
            "created_date",
            "updated_date",
            "placed_date",
            "vendor",
            "cart",
            
    
        ]
        depth = 1


class CouponSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
    
        fields = '__all__'
    
class OrderStepsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = OrderSteps
    
        fields = '__all__'


class VendorOrderSerialzer(serializers.ModelSerializer):

    cart = CartSerialzer(many =True)
    class Meta:
        model = Order
        
        fields = [
            "id",

            "user" ,
            "order_id", 
            "order_status",
            "ammount",
            "address", 
            "is_paid", 
            "payment_details",
            "created_date",
            "updated_date",
            "placed_date",
            # "vendor",
            "cart",
            
    
        ]
        depth = 1
    