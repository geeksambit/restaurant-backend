from django.db import models
from user.models import *

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    image = models.CharField(blank=True,max_length=200)
    is_active = models.CharField(max_length=1)
    vendor =models.ForeignKey(Vendor,on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name
    @property
    def product(self):
        return self.product_set.all()



class Cuisine(models.Model):
    cuisine_name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    is_active = models.CharField(max_length=1)

    def __str__(self):
        return self.cuisine_name
    @property
    def product(self):
        return self.product_set.all()


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    is_active = models.CharField(max_length=1)
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    cuisine =models.ForeignKey(Cuisine,on_delete=models.CASCADE)
    is_veg = models.CharField(max_length=1)
    
    price = models.CharField(max_length=200)
    description = models.CharField(blank=True,max_length=200)
    
    

    def __str__(self):
        return self.product_name

