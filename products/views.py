from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import *
from products.serializers import *
import base64
from  utils import common

# Create your views here.


class CategoryView(APIView):

    def get(self, request):
        data =request.GET.get('vendor_id', '')
        queryset=Category.objects.filter(vendor_id=data)
        # queryset=Category.objects.all()
        serializer = CategorySerialzer(queryset,many= True)
        # print (repr(serializer))
        return Response({"data":serializer.data,"status":"00","message":"success"}, status=200)
    
    def post(self, request):
         data = request.data
         serializer = CategorySerialzer(data=data)
         if serializer.is_valid():
             serializer.save()
             return Response({"data":serializer.data,"status":"00","message":"success"},status=201)
         return Response({"data":serializer.errors,"status":"01","message":"success"}, status=400)



class CategoryDetailsView(APIView):
    def get_object(self,id= None):
         try:
            return Category.objects.get(id=id)
            
         except Category.DoesNotExist as e:
            return Response({"error": "Given category not found."}, status=404)   
    
    def get(self, request, id=None):

        instance = self.get_object(id)
        serailizer = CategorySerialzer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = CategorySerialzer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"status":"00","message":"success"}, status=200)
        return Response({"data":serializer.errors,"status":"01","message":"success"}, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return Response({"data":None,"status":"00","message":"success"},status=204)

class CuisineView(APIView):

    def get(self, request):
        queryset=Cuisine.objects.all()
        serializer = CuisineSerialzer(queryset,many= True)
        # print (repr(serializer))
        return Response({"data":serializer.data,"status":"00","message":"success"})
    
    def post(self, request):
         data = request.data
         serializer = CuisineSerialzer(data=data)
         if serializer.is_valid():
             serializer.save()
             return Response({"data":serializer.data,"status":"00","message":"success"},status=201)
         return Response({"data":serializer.errors,"status":"01","message":"Failed"}, status=400) 
    
class CuisineDetailsView(APIView):
    def get_object(self,id= None):
         try:
            return Cuisine.objects.get(id=id)
            
         except Cuisine.DoesNotExist as e:
            return Response({"error": "Given category not found."}, status=404)   
    
    def get(self, request, id=None):

        instance = self.get_object(id)
        serializer = CuisineSerialzer(instance)
        return Response({"data":serializer.data,"status":"00","message":"success"})

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = CuisineSerialzer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"status":"00","message":"success"}, status=200)
        return Response({"data":serializer.errors,"status":"00","message":"success"}, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return Response({"data":None,"status":"00","message":"success"},status=204)


class ProductsView(APIView):

    def get(self, request):
        queryset=Product.objects.all()
        serializer = ProductSerialzer(queryset,many= True)
        # print (repr(serializer))
        return Response({"data":serializer.data,"status":"00","message":"success"})
    
    def post(self, request):
        data = request.data

        img_data = data["image"]
        # import pdb;pdb.set_trace()
        s1 = img_data.encode("ascii")
        image_name = common.get_rand()+'.png'
        data["image"]=image_name
        with open("../ammus2/{}".format(image_name), "wb") as fh:
            fh.write(base64.decodebytes(s1))
        
         
        serializer = ProductSerialzer(data=data)
        if serializer.is_valid():

            serializer.save()
            return Response({"data":serializer.data,"status":"00","message":"success"},status=201)
        return Response({"data":serializer.errors,"status":"01","message":"success"}, status=400)

class ProductDetailsViews(APIView):
    def  get_object(self,id= None):
         try:
            return Product.objects.get(id=id)
            
         except Product.DoesNotExist as e:
             obj = Product()
             return obj   
    
    def get(self, request, id=None):

        #instance = self.get_object(id)
        instance = self.get_object(id)
        serializer = ProductSerialzer(instance)
        return Response({"data":serializer.data,"status":200,"message":"ok"})  
    
    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = ProductSerialzer(instance, data=data)
        img_data = data["image"]
        # import pdb;pdb.set_trace()
        s1 = img_data.encode("ascii")
        image_name = common.get_rand()+'.png'
        data["image"]=image_name
        with open("../ammus2/{}".format(image_name), "wb") as fh:
            fh.write(base64.decodebytes(s1))
        

        if serializer.is_valid():
            serializer.save()
            return Response({"data":"aa","status":"00","message":"Success"}, status=200)
        return Response({"data":serializer.errors,"status":"01","message":"Failed"}, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return Response({"data":None,"status":"00","message":"success"},status=204)


class ProductCuisineViews(APIView):
    def  get_object(self,id= None):
         try:
            return Cuisine.objects.get(id=id)
            
         except Cuisine.DoesNotExist as e:
             obj = Product()
             return obj   
    
    def get(self, request, id=None):

        #instance = self.get_object(id)
        instance = self.get_object(id)
        serializer = ProductByCuisineSerialzer(instance)
        return Response({"data":serializer.data,"status":"00","message":"Success"})  


class ProductsByCategory(APIView):

    def post(self, request):

        data = request.data
        #queryset = Product.objects.all()
        queryset = Product.objects.filter(category=data["category"])
        #queryset=Combo.objects.filter(id=1).select_related()
        serializer = ProductSerialzer(queryset,many= True)
        
        all_product=serializer.data
                
        return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)


class AllProductsByCategory(APIView):

    def post(self, request):
        data = request.data
        # queryset = Category.objects.all()
        queryset = Category.objects.filter(vendor_id=data["vendor_id"])
        
        serializer = AllProductsByCategorySerilizer(queryset,many= True)
        all_product=serializer.data
        return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)



class AllProductsByCusine(APIView):

    def get(self, request):
        queryset = Cuisine.objects.all()
        serializer = ProductByCuisineSerialzer(queryset,many= True)
        all_product=serializer.data
        return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)


    
