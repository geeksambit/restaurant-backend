from django.db import models
from user.models import *
from products.models import *

# Create your models here.


class OrderSteps(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name



class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.CharField(blank=True,max_length=200)
    order_status = models.ForeignKey(OrderSteps,on_delete=models.CASCADE)
    ammount = models.CharField(blank=True,max_length=200)
    address =models.CharField(blank=True,max_length=200)
    is_paid = models.CharField(default='0',max_length=200)
    payment_details = models.CharField(blank=True,max_length=200)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True)
    placed_date =models.DateTimeField(blank=True,null=True)
    total_tax =models.CharField(blank=True,max_length=200)
    discount =models.CharField(blank=True,max_length=200)
    total_price =models.CharField(blank=True,max_length=200)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(DeliveryBoy,on_delete=models.CASCADE,blank=True, null=True)
    trasaction_id = models.CharField(blank=True,null=True,max_length=200)
    

    def __str__(self):
        return self.id

    @property
    def cart(self):
        return self.cart_set.all()

class Cart(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)
    ammount = models.CharField(max_length=200)
    is_ordered = models.BooleanField(default = False)
    order_status = models.ForeignKey(OrderSteps,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return self.order_status


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=200)
    discount_persentage = models.CharField(blank=True,max_length=200)
    is_active = models.CharField(max_length=1)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)


    def __str__(self):
        return self.coupon_code

