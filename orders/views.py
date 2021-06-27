from django.shortcuts import render

from django.shortcuts import render
from rest_framework.views import APIView
from orders.models import *
from user.models import *
from products.models import *
from orders.serializers import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from utils import dbcon
import datetime
import datetime
from datetime import timedelta

from  utils import common

# Create your views here.


class AddToCartView(APIView):

    def post(self, request):
        carts = request.data
        #import pdb;pdb.set_trace()
        
        get_order = dbcon.execute("SELECT * FROM orders_order where user_id = {} and order_status_id = {} and vendor_id= {}".format(carts["user_id"],'1',carts["vendor_id"]))

        if not get_order: 

            
            create_order = dbcon.execute(" insert INTO `orders_order`( `order_status_id`, `user_id`,`vendor_id`) VALUES ('1',{},{})".format(carts["user_id"],carts["vendor_id"]))
            cart_data = carts["cart"]
            for cd in cart_data:
                product_id = cd["product_id"]
                quantity = cd["quantity"]
                price = dbcon.execute(" SELECT * FROM `products_product` WHERE `id`={} ".format(product_id))[0]['price']
                amount = int(quantity) * int(price)
                #import pdb;pdb.set_trace()

                add_to_cart = dbcon.execute(" insert INTO `orders_cart`( `quantity`, `ammount`, `product_id`, `order_id`, `order_status_id`,`is_ordered`) VALUES ({},{},{},{},{},{}) ".format(quantity,amount,product_id,create_order,1,0))
          
        else :
            cart_data = carts["cart"]
            #order_id = dbcon.execute("")
            order_id= get_order[0]["id"]
            for cd in cart_data:
                product_id = cd["product_id"]
                cart_data = dbcon.execute("SELECT id,`quantity`,order_id FROM `orders_cart` WHERE `product_id`={} AND `order_status_id`=1 AND orders_cart.order_id= {} AND `is_ordered`=0".format(product_id,order_id))
                #import pdb;pdb.set_trace()               
                if cart_data:
                    quantity_in_cart = cart_data[0]["quantity"]
                    cart_id = cart_data[0]["id"]
                    order_id = cart_data[0]["order_id"]
                    #import pdb;pdb.set_trace()
                    price = dbcon.execute("SELECT * FROM `products_product` WHERE `id`={} ".format(product_id))[0]['price']
                    
                    new_quantity = int(quantity_in_cart) + int(cd["quantity"])
                    amount = new_quantity * int(price)
                    update_cart = dbcon.execute("UPDATE `orders_cart` SET `quantity`={},`ammount`={} WHERE `id`={}".format(new_quantity,amount,cart_id))
                    #import pdb;pdb.set_trace()
                else :
                    product_id = cd["product_id"]
                    quantity = cd["quantity"]
                    
                    price = dbcon.execute("SELECT * FROM products_product WHERE `id`={}".format(product_id))[0]["price"]
                    
                    amount = int(quantity) * int(price)
                    #import pdb;pdb.set_trace()
                    add_to_cart = dbcon.execute("INSERT INTO `orders_cart`( `quantity`, `ammount`, `product_id`, `order_id`, `order_status_id`, `is_ordered`) VALUES ({},{},{},{},{},{}) ".format(quantity,amount,product_id,order_id,1,0))
        

        cart_data= dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={})".format(carts["user_id"],'1'))
        other_data= dbcon.execute("SELECT SUM(orders_cart.`ammount`) as ammount,5 as tax_persentage ,SUM(orders_cart.`ammount`)*5/100 as total_tax,SUM(orders_cart.`ammount`)+SUM(orders_cart.`ammount`)*5/100 as total_price FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={})".format(carts["user_id"],'1'))[0]
        #cart_data= dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={})".format(carts["user_id"],'1'))
        #response_data ={"cart_data":cart_data}
        coupons_data = dbcon.execute("SELECT * FROM `orders_coupon` WHERE 1")
        response_data ={"cart_data":cart_data,"coupons":coupons_data}
        response_data.update(other_data)
        #import pdb;pdb.set_trace()
        return Response(  {"data":response_data,"status":"00","message":"Success"}, status=200)

class ApplyCouponsView(APIView):
    def post(self, request):

        data = request.data
        user_id = data["user_id"]
        coupon_id = data["coupon_id"]
        vendor_id = data["vendor_id"]
         
        coupon_discount= dbcon.execute("SELECT * FROM `orders_coupon` WHERE `id`={}".format(coupon_id))[0]['discount_persentage']
       

        cart_data= dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id={})".format(user_id,'1',vendor_id))
        other_data= dbcon.execute("SELECT SUM(orders_cart.`ammount`) as ammount,5 as tax_persentage ,SUM(orders_cart.`ammount`)*5/100 as total_tax,SUM(orders_cart.`ammount`)+SUM(orders_cart.`ammount`)*5/100 as total_price FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id={})".format(user_id,'1',vendor_id))[0]
        
        price =other_data["ammount"]
        total_tax = other_data["total_tax"]
        discount = price * int(coupon_discount)/100
        final_price = price + total_tax - discount
        #import pdb;pdb.set_trace()
        other_data.update({"discount":discount,"total_price":final_price})
        
        #update_order_data = dbcon.execute("UPDATE `orders_order` SET `ammount`={},`discount`={},`total_price`={},`total_tax`={} WHERE `user_id`={} and `order_status_id`=1".format(price,discount,final_price,total_tax,user_id))
        response_data ={"cart_data":cart_data}
        #order_data = dbcon.execute("SELECT `ammount`,`discount`,`total_tax`,`total_price` FROM `orders_order` WHERE `user_id`={} and `order_status_id`=1".format(user_id))[0]
        response_data.update(other_data)
        if response_data :
            return Response({"data":response_data,"status":"00","message":"Success"}, status=200)
        else :
            return Response({"false"})

        
class OrderPlaceView(APIView):
    
    def post(self, request):
        data = request.data
        address_id = data["address"]
        address = dbcon.execute("SELECT * FROM `user_shippingadress` WHERE `id`={}".format(int(address_id)))
        name =address[0]["name"]
        mobile=address[0]["mobile_no"]
        pin=address[0]["pin"]
        locality=address[0]["locality"]
        city=address[0]["city"]
        state=address[0]["state"]
        landmark=address[0]["landmark"]
        address ="name -"+ name +",locality -"+locality +",pin -"+pin +",city -"+city +",landmark -"+landmark +",mobile -"+mobile
        

        #import pdb;pdb.set_trace()
        user_id = data["user_id"]
        is_paid = data["is_paid"]
        vendor_id = data["vendor_id"]
        #coupon_id = data["coupon_id"]
        
        payment_details =data["payment_details"]
        placed_date  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_id = common.get_order_no() 
        print (order_id)


        # import pdb;pdb.set_trace()
        
        get_order= dbcon.execute("SELECT * FROM `orders_order` WHERE `user_id`= {} AND `order_status_id`=1 AND `vendor_id`={}".format(user_id,vendor_id))[0]["id"]
        # import pdb;pdb.set_trace()
        cart_data = dbcon.execute("SELECT `id`,`product_id`,`ammount`FROM `orders_cart` WHERE `order_id`= {} AND `order_status_id`= 1 AND `is_ordered`= 0".format(get_order))
        ammount = 0
        

        for cd in cart_data:
            ammount = ammount+ int(cd["ammount"])
            place_order_cart = dbcon.execute("UPDATE `orders_cart` SET `order_status_id`=2 ,`is_ordered`= 1 WHERE `id`={}".format(cd["id"]))
        #import pdb;pdb.set_trace()
        #
        if  data["coupon_id"]:
            coupon_discount= dbcon.execute("SELECT * FROM `orders_coupon` WHERE `id`={}".format(data["coupon_id"]))[0]['discount_persentage']
        else:
            coupon_discount =0


        total_tax =ammount * 5/100
        discount = ammount * int(coupon_discount)/100
        final_price = ammount + total_tax - discount
        #import pdb;pdb.set_trace()
        trasaction_id =data["trasaction_id"]



        
        order_place = dbcon.execute("UPDATE `orders_order` SET `order_id`='{}',`ammount`='{}',`address`='{}',`is_paid`='{}',`placed_date`='{}',`payment_details`= '{}',`order_status_id`=2,total_price={},total_tax={},discount={} ,`trasaction_id`='{}' WHERE `id`= {}".format(order_id,ammount,address,is_paid,placed_date,payment_details,final_price,total_tax,discount,trasaction_id ,get_order))
        cart_data =dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.id= {})".format(get_order))
        response_data ={"cart_data":cart_data}
        other_data= dbcon.execute("SELECT * FROM `orders_order` WHERE id = {}".format(get_order))[0]
        response_data.update(other_data)
        return Response({"data":response_data,"status":"00","message":"Success"}, status=200)


        #q = "UPDATE `orders_order` SET `ammount`='{}',`address`='{}',`is_paid`='{}',`payment_details`= '{}',`order_status_id`=2,total_price='{}',total_tax='{}',discount='{}' WHERE `id`= {}".format(ammount,address,is_paid,payment_details,final_price,total_tax,discount,get_order)
        # order_place = dbcon.execute("UPDATE `orders_order` SET `ammount`='{}',`address`='{}',`is_paid`='{}',`payment_details`= '{}',`order_status_id`=2,total_price={},total_tax={},discount={} WHERE `id`= {}".format(ammount,address,is_paid,payment_details,final_price,total_tax,discount,get_order))
        # cart_data =dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.id= {})".format(get_order))
        # response_data ={"cart_data":cart_data}
        # other_data= dbcon.execute("SELECT * FROM `orders_order` WHERE id = {}".format(get_order))[0]
        # response_data.update(other_data)
        # return Response({"data":response_data,"status":"00","message":"Success"}, status=200)

    


class CartDataView(APIView):
    def post(self, request):

        data = request.data
        user_id = data["user_id"]
        vendor_id = data["vendor_id"]

        cart_data= dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id={})".format(user_id,'1',vendor_id))
        other_data= dbcon.execute("SELECT SUM(orders_cart.`ammount`) as ammount,5 as tax_persentage ,SUM(orders_cart.`ammount`)*5/100 as total_tax,SUM(orders_cart.`ammount`)+SUM(orders_cart.`ammount`)*5/100 as total_price FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id={} )".format(user_id,'1',vendor_id))[0]
        coupons_data = dbcon.execute("SELECT * FROM `orders_coupon` WHERE 1")
        response_data ={"cart_data":cart_data,"coupons":coupons_data}
        response_data.update(other_data)
        
        return Response({"data":response_data,"status":"00","message":"Success"}, status=200)




class UpdateCartDataView(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()

        product_id = data["update_cart"]["product_id"]
        cart_id = data["update_cart"]["id"]
        user_id = data["user_id"]
        vendor_id = data["vendor_id"]

        #quantity_in_cart = cart_data[0]["quantity"]cart_id = cart_data[0]["id"]
        #order_id = cart_data[0]["order_id"]
        
        price = dbcon.execute("SELECT * FROM `products_product` WHERE `id`={} ".format(product_id))[0]['price']        

        new_quantity = int(data["update_cart"]["quantity"])
        amount = new_quantity * int(price)
        update_cart = dbcon.execute("UPDATE `orders_cart` SET `quantity`={},`ammount`={} WHERE `id`={}".format(new_quantity,amount,cart_id))
        

        cart_data= dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id= {})".format(user_id,'1',vendor_id))
        coupons_data = dbcon.execute("SELECT * FROM `orders_coupon` WHERE 1")
        response_data ={"cart_data":cart_data,"coupons":coupons_data}
        other_data= dbcon.execute("SELECT SUM(orders_cart.`ammount`) as ammount,5 as tax_persentage ,SUM(orders_cart.`ammount`)*5/100 as total_tax,SUM(orders_cart.`ammount`)+SUM(orders_cart.`ammount`)*5/100 as total_price FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id={})".format(user_id,'1',vendor_id))[0]
        #import pdb;pdb.set_trace()
        response_data.update(other_data)
        return Response({"data":response_data,"status":"00","message":"Success"}, status=200)


class DeleteCartDataView(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()

        product_id = data["update_cart"]["product_id"]
        cart_id = data["update_cart"]["id"]
        user_id = data["user_id"]
        vendor_id = data["vendor_id"]

       
        delete_cart = dbcon.execute("DELETE FROM `orders_cart` WHERE `id`= {}".format(cart_id))
        

        cart_data= dbcon.execute("SELECT orders_cart.`id`,orders_cart.`quantity`,orders_cart.`ammount`,`product_id`,products_product.price,products_product.product_name,products_product.image FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id= {})".format(user_id,'1',vendor_id))
        coupons_data = dbcon.execute("SELECT * FROM `orders_coupon` WHERE 1")
        response_data ={"cart_data":cart_data,"coupons":coupons_data}
        other_data= dbcon.execute("SELECT SUM(orders_cart.`ammount`) as ammount,5 as tax_persentage ,SUM(orders_cart.`ammount`)*5/100 as total_tax,SUM(orders_cart.`ammount`)+SUM(orders_cart.`ammount`)*5/100 as total_price FROM `orders_cart` INNER JOIN products_product ON products_product.id=orders_cart.product_id WHERE `order_id` IN (SELECT id FROM orders_order WHERE orders_order.user_id={} AND orders_order.order_status_id={} AND orders_order.vendor_id={})".format(user_id,'1',vendor_id))[0]
        #import pdb;pdb.set_trace()
        response_data.update(other_data)

        return Response({"data":response_data,"status":"00","message":"Success"}, status=200)


class CouponsView(APIView):
    def post(self, request):
        data =request.data
        queryset = Coupon.objects.filter(vendor_id=data["vendor_id"])
        serializer = CouponSerialzer(queryset,many= True)

        
        return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)



class OrderHistoryView(APIView):

    def post(self, request):
        data= request.data
        queryset = Order.objects.filter(user_id=data["user_id"]).order_by('-id')
        serializer = OrderSerialzer(queryset,many= True)
        all_product=serializer.data
        return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)


class AssignDeliveryboy(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()

        order_id = data["order_id"]
        deliveryboy_id = data["deliveryboy_id"]
        assgn_deliveryboy =  dbcon.execute("UPDATE `orders_order` SET `delivery_boy_id`={},`order_status_id`=4 WHERE `id`={}".format(deliveryboy_id,order_id))
        if assgn_deliveryboy :
            return Response({"data":True,"status":"00","message":"Success"}, status=200)
        else :
            return Response({"data":False,"status":"00","message":"Failled"}, status=200)


class AcceptOrder(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()

        order_id = data["order_id"]
        assgn_deliveryboy =  dbcon.execute("UPDATE `orders_order` SET `order_status_id`=3 WHERE `id`={}".format(order_id))
        if assgn_deliveryboy :
            return Response({"data":True,"status":"00","message":"Success"}, status=200)
        else :
            return Response({"data":False,"status":"00","message":"Failled"}, status=200)

class Outfordeliovery(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()

        order_id = data["order_id"]
        assgn_deliveryboy =  dbcon.execute("UPDATE `orders_order` SET `order_status_id`=5 WHERE `id`={}".format(order_id))
        if assgn_deliveryboy :
            return Response({"data":True,"status":"00","message":"Success"}, status=200)
        else :
            return Response({"data":False,"status":"00","message":"Failled"}, status=200)
class Deliverd(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()
        order_id = data["order_id"]
        assgn_deliveryboy =  dbcon.execute("UPDATE `orders_order` SET `order_status_id`=6 WHERE `id`={}".format(order_id))
        if assgn_deliveryboy :
            return Response({"data":True,"status":"00","message":"Success"}, status=200)
        else :
            return Response({"data":False,"status":"00","message":"Failled"}, status=200)

class VendorWiseOrders(APIView):

    def post(self, request):
        data= request.data
        queryset = Order.objects.filter(vendor_id=data["vendor_id"],order_status_id=data["order_status_id"]).order_by('-id')
        serializer = VendorOrderSerialzer(queryset,many= True)
        all_product=serializer.data
        return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)


class OrderSteps(APIView):

    def get(self, request):
        order_steps = dbcon.execute("select * FROM `orders_ordersteps` WHERE `id`>1")
        # serializer = OrderStepsSerialzer(queryset,many= True)
        # print (repr(serializer))
        return Response({"data":order_steps,"status":"00","message":"success"})

class HistroryByDate(APIView):

    def post(self, request):
        data= request.data
        vendor_id=data["vendor_id"]
        order_status_id=data["order_status_id"]
        from_date =data["from_date"]
        end_date = data["end_date"]
        order_steps = dbcon.execute("SELECT * FROM `orders_order` WHERE `order_status_id`={} AND`vendor_id`={} AND `placed_date` BETWEEN '{}' AND '{}'".format(order_status_id,vendor_id,from_date,end_date))
        # queryset = Order.objects.filter(vendor_id=data["vendor_id"],order_status_id=data["order_status_id"],placed_date__range=["2011-01-01", "2011-01-31"]).order_by('-id')
        # serializer = VendorOrderSerialzer(queryset,many= True)
        # all_product=serializer.data
        if order_steps:

            return Response({"data":order_steps,"status":"00","message":"Success"}, status=200)

        else:
            return Response({"data":order_steps,"status":"01","message":"No data found"}, status=200)



class CancelOrder(APIView):
    def post(self, request):

        data = request.data
        #import pdb;pdb.set_trace()

        order_id = data["order_id"]
        assgn_deliveryboy =  dbcon.execute("UPDATE `orders_order` SET `order_status_id`=8 WHERE `id`={}".format(order_id))
        if assgn_deliveryboy :
            return Response({"data":True,"status":"00","message":"Success"}, status=200)
        else :
            return Response({"data":False,"status":"00","message":"Failled"}, status=200)

    



