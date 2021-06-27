from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    salt = models.CharField(blank=True,max_length=200)
    jwt_token = models.CharField(blank=True,max_length=500)
    reset_password= models.CharField(default=0,max_length=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True)
    social_id = models.CharField(blank=True,max_length=200)
    fcm_id = models.CharField(blank=True,default=None,max_length=500)
    

    def __str__(self):
        return self.name
    
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    address = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    image = models.CharField(default=None,max_length=200)
    fcm_id = models.CharField(blank=True,default=None,max_length=500)



    def __str__(self):
        return self.name

class ShippingAdress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    locality= models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    landmark = models.CharField(default=None,max_length=200)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DeliveryBoy(models.Model):
    name = models.CharField(max_length=200)
    # email = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    # password = models.CharField(max_length=200)
    # reset_password= models.CharField(default=0,max_length=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True)
    address = models.CharField(max_length=200)
    route = models.CharField(max_length=200,default=None,blank=True)

    def __str__(self):
        return self.name
