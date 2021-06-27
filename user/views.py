from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import *
from .serializers import *
from rest_framework import status
import jwt
import bcrypt
from django.conf import settings
from utils.decorators import is_login
from utils.common import response
from utils import dbcon
# import zerosms
# from twilio.rest import Client 
import smtplib
from  utils import common


# Create your views here.
class UserView(APIView):

    @is_login
    def get(self, request):
        print("inside get")
        queryset=User.objects.all()
        serializer = UserSerialzer(queryset,many= True)
        # print (repr(serializer))
        return Response(serializer.data)



from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

class RegisterView(APIView):
    def post(self, request):
        #return Response(settings.BCRYPT_SECRECT)


        data = request.data
        try :
            queryset = User.objects.get(email=data["email"])
            if queryset :
                return Response({"data":None,"status":"01","message":"email exists"}, status=200)
        
        except User.DoesNotExist as e:

            #return  Response({"data":None,"status":203,"message":"email dose not exist"}, status=200) 

            salt = bcrypt.gensalt()
            #data["salt"] = salt.decode("utf-8")
            data["salt"] = salt
            hashed = bcrypt.hashpw(request.data["password"].encode("utf-8"), salt)
            data["password"] = hashed
            #data["password"] = hashed.decode("utf-8")
            
            serializer = UserSerialzer(data=data)
            if serializer.is_valid():
                serializer.save()
    
                payload = {
                    'user_id': serializer.data["id"],
                    'email': serializer.data["email"]
                }
                encoded = jwt.encode(payload, settings.JWT_SECRECT, algorithm='HS256').decode("utf-8")
                User.objects.filter(pk=serializer.data["id"]).update(jwt_token=encoded)
                queryset= User.objects.get(pk=serializer.data["id"])
                serializer = UserSerialzer(queryset)

                return Response({"data":serializer.data,"status":"00","message":"Success"})
            return Response({"data":serializer.errors, "status":"01","message":"Failed"})




class LoginView(APIView):

    def post(self, request):
        try:
            user = request.data
            #email =  get_object_or_404(User, email=user["email"])
            email = User.objects.get(email=user["email"])
            serializer = UserSerialzer(email)
        

            if serializer.data["name"]:
                email = serializer.data["email"]
                passwd = serializer.data["password"]
                salt = serializer.data["salt"].encode("utf-8")
		#salt = serializer.data["salt"]
                hashed = bcrypt.hashpw(user["password"].encode('utf-8'), salt)
                
                if passwd == hashed:
                   #passwd == hashed.decode("utf-8") :

                    payload = {
                    'user_id': serializer.data["id"],
                    'email': serializer.data["email"]
                    }
                    encoded = jwt.encode(payload, settings.JWT_SECRECT, algorithm='HS256').decode("utf-8")
                    User.objects.filter(pk=serializer.data["id"]).update(jwt_token=encoded)
                    queryset= User.objects.get(pk=serializer.data["id"])
                    serializer = LoginSerializer(queryset)
                    
                    return Response({"data":serializer.data,"status":"00","message":"You are logged in"}, status=200)
                    
                else :
                    return Response({"data":None,"status":"01","message":"Wrong Password"}, status=200)

                
        except User.DoesNotExist as e:
            return  Response({"data":None,"status":"01","message":"email dose not exist"}, status=200) 



class ShippingAddress(APIView):

    def post(self, request):
        data = request.data

        name = data["name"]
        mobile_no = data["mobile_no"]
        pin = data["pin"]
        locality = data["locality"]
        city = data["city"]
        state =data["state"]
        landmark= data["landmark"]
        user_id = data["user_id"]
        longitude =data["longitude"]
        latitude = data["latitude"]
        #import pdb;pdb.set_trace()
        

        insert_to_address = dbcon.execute("insert INTO `user_shippingadress`( `name`, `mobile_no`, `pin`, `locality`, `city`, `state`, `landmark`, `user_id`,longitude,latitude) VALUES ('{}','{}','{}','{}','{}','{}','{}',{},{},{}) ".format(name,mobile_no,pin,locality,city,state,landmark,user_id,longitude,latitude))
        response_data = dbcon.execute("SELECT * FROM `user_shippingadress` WHERE `user_id`={}".format(user_id))
        if insert_to_address :

            return Response({"data":response_data,"status":"00","message":"succes"}, status=200)
        else :
            return Response({"data":None,"status":"01","message":"Failed"}, status=200)

class UserAddress(APIView):

    def post(self, request):
        data = request.data

        user_id = data["user_id"]
        #import pdb;pdb.set_trace()
        

        address = dbcon.execute("SELECT * FROM `user_shippingadress` WHERE `user_id`= {}".format(user_id))

        if address :

            return Response({"data":address,"status":"00","message":"succes"}, status=200)
        else :
            return Response({"data":None,"status":"01","message":"No Address Found"}, status=200)

class UpdateAddress(APIView):

    def post(self, request):
        data = request.data

        name = data["name"]
        mobile_no = data["mobile_no"]
        pin = data["pin"]
        locality = data["locality"]
        city = data["city"]
        state =data["state"]
        landmark= data["landmark"]
        longitude =data["longitude"]
        latitude = data["latitude"]
        id =  data["id"]
        #import pdb;pdb.set_trace()
        

        upadate_address = dbcon.execute("UPDATE `user_shippingadress` SET `name`='{}',`mobile_no`='{}',`pin`='{}',`locality`='{}',`city`='{}',`state`='{}',`landmark`='{}',`longitude`='{}',`latitude`='{}'  WHERE `id`={}".format(name,mobile_no,pin,locality,city,state,landmark,longitude,latitude,id))

        if upadate_address :

            return Response({"data":None,"status":"00","message":"succes"}, status=200)
        else :
            return Response({"data":None,"status":"01","message":"Failed"}, status=200)

         
class VendorsView(APIView):

    def get(self, request):
        print("inside get")
        queryset=Vendor.objects.all()
        serializer = VendorSerializer(queryset,many= True)
        # print (repr(serializer))
        return Response({"data":serializer.data,"status":"00","message":"succes"}, status=200)

class UpdateProfile(APIView):

    def post(self, request):
        data = request.data

        name = data["name"]
        mobile_no = data["mobile_no"]
        # email = data["email"]
        user_id =  data["user_id"]

        #profile_update = dbcon.execute("UPDATE `user_user` SET `name`={},`mobile_no`={} WHERE `id`={} ".format(name,mobile_no,user_id))
        upadate_address = dbcon.execute("UPDATE `user_user` SET `name`= '{}',`mobile_no`={} WHERE `id`={}".format(name,mobile_no,user_id))
        #import pdb;pdb.set_trace()
        if upadate_address :
            return Response({"data":None,"status":"00","message":"succes"}, status=200)
        else :
            return Response({"data":None,"status":"01","message":"Failed"}, status=202)

class DeleteAddress(APIView):

    def post(self, request):
        data = request.data
        id =  data["id"]

       
        upadate_address = dbcon.execute("DELETE FROM `user_shippingadress` WHERE `id`={}".format(id))
        #import pdb;pdb.set_trace()
        return Response({"data":None,"status":"00","message":"succes"}, status=200)


class UpdatePassword(APIView):

    def post(self, request):
        data = request.data

        old_password = data["old_password"]
        new_password = data["new_password"]
        # email = data["email"]
        user_id =  data["user_id"]
        # check_password = 

        #profile_update = dbcon.execute("UPDATE `user_user` SET `name`={},`mobile_no`={} WHERE `id`={} ".format(name,mobile_no,user_id))
        upadate_address = dbcon.execute("UPDATE `user_user` SET `name`= '{}',`mobile_no`={} WHERE `id`={}".format(name,mobile_no,user_id))
        #import pdb;pdb.set_trace()
        if upadate_address :
            return Response({"data":None,"status":"00","message":"succes"}, status=200)
        else :
            return Response({"data":None,"status":"01","message":"Failed"}, status=202)





class VendorLogin(APIView):

    def post(self, request):

        try:
            user = request.data
            email = Vendor.objects.get(email=user["email"])
            serializer = VendorSerializer(email)
        

            if email:
                email = serializer.data["email"]
                passwd = serializer.data["password"]
                
                if passwd == user["password"]:

                    queryset= Vendor.objects.get(pk=serializer.data["id"])
                    serializer = VendorLoginSerializer(queryset)
                    
                    return Response({"data":serializer.data,"status":"00","message":"You are logged in"}, status=200)
                    
                else :
                    return Response({"data":None,"status":"01","message":"Wrong Password"}, status=200)

        except User.DoesNotExist as e:

            return  Response({"data":None,"status":"01","message":"email dose not exist"}, status=200) 


class Deliveryboy(APIView):

    def get(self, request):
        print("inside get")
        queryset=DeliveryBoy.objects.all()
        serializer = DeliveryBoySerializer(queryset,many= True)
        # print (repr(serializer))
        return Response({"data":serializer.data,"status":"00","message":"succes"}, status=200)

    def post(self, request):
         data = request.data
         serializer = DeliveryBoySerializer(data=data)
         if serializer.is_valid():
             serializer.save()
             return Response({"data":serializer.data,"status":"00","message":"success"},status=201)
         return Response({"data":serializer.errors,"status":"01","message":"success"}, status=400)


class DeliveryboyDetailsViews(APIView):
    def  get_object(self,id= None):
         try:
            return DeliveryBoy.objects.get(id=id)
            
         except DeliveryBoy.DoesNotExist as e:
             obj = Product()
             return obj   
    
    def get(self, request, id=None):

        #instance = self.get_object(id)
        instance = self.get_object(id)
        serializer = DeliveryBoySerializer(instance)
        return Response({"data":serializer.data,"status":200,"message":"ok"})  
    
    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = DeliveryBoySerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"status":"00","message":"Success"}, status=200)
        return Response({"data":serializer.errors,"status":"01","message":"Failed"}, status=400)





class GoogleLogin(APIView):
    def post(self, request):
        user = request.data
        id_token=user["id_token"]
        name=user["name"]
     
        email=user["email"]
        google_id=user["google_id"]
        mobile_no= "0000000000"
        password = "capialpass"

        get_user =  dbcon.execute("SELECT * FROM `user_user` WHERE `social_id`={}".format(google_id))
        if not get_user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password.encode("utf-8"), salt)
            payload = {
                    'user_id': google_id,
                    'email': email
                }
            jwt_token = jwt.encode(payload, settings.JWT_SECRECT, algorithm='HS256').decode("utf-8")
            inser_user = dbcon.execute("insert INTO `user_user`( `name`, `email`, `mobile_no`, `password`, `salt`, `jwt_token`,`social_id`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(name,email,mobile_no,password,salt,jwt_token,google_id))
            if inser_user:

                response_data =dbcon.execute("SELECT * FROM `user_user` WHERE `social_id`={}".format(google_id))
                return Response({"data":response_data,"status":"00","message":"You are reg/logged in"}, status=200)
            else :
                serializer = UserSerialzer(email)

                if serializer.data["name"]:
                    email = serializer.data["email"]
                    passwd = serializer.data["password"]
                    salt = serializer.data["salt"].encode("utf-8")
                    hashed = bcrypt.hashpw(user["password"].encode('utf-8'), salt)
                   
                    if passwd == hashed:

                        payload = {
                        'user_id': serializer.data["id"],
                        'email': serializer.data["email"]
                        }
                        encoded = jwt.encode(payload, settings.JWT_SECRECT, algorithm='HS256').decode("utf-8")
                        User.objects.filter(pk=serializer.data["id"]).update(jwt_token=encoded)
                        queryset= User.objects.get(pk=serializer.data["id"])
                        serializer = LoginSerializer(queryset)
                        
                        return Response({"data":serializer.data,"status":"00","message":"You are logged in"}, status=200)
                        
                    else :
                        return Response({"data":None,"status":"01","message":"Wrong Password"}, status=200)

        else:
            response_data =dbcon.execute(" SELECT * FROM `user_user` WHERE `social_id`={}".format(google_id))[0]
            return Response({"data":response_data,"status":"00","message":"You are logged in"}, status=200)

# class FogotPass(APIView):

#     def post(self, request):
        
 
        

#         from twilio.rest import Client

#         account_sid = 'AC5a0822dee37358c8f5e45a9a1a328d52' # Found on Twilio Console Dashboard
#         auth_token = 'cc4ce037cef4c30ea48e36d98a19d59c' # Found on Twilio Console Dashboard

#         myPhone = '+919437160193' # Phone number you used to verify your Twilio account
#         TwilioNumber = '+16267142799' # Phone number given to you by Twilio

#         client = Client(account_sid, auth_token)

#         x = client.messages.create(
#         to=myPhone,
#         from_=TwilioNumber,
#         body='I sent a text message from Python! ' + u'\U0001f680')

#         print(x)


#         return Response({"data":"ss","status":"01","message":"success"}, status=200)

class FogotPass(APIView):

    def post(self, request):
        data = request.data
        email = data["email"]
        get_user =  dbcon.execute("SELECT * FROM `user_user` WHERE `email`='{}'".format(email))
        # print(get_user)

        if get_user:
            salt = bcrypt.gensalt()

            passwd = common.get_order_no()
            hashed = bcrypt.hashpw(passwd.encode("utf-8"), salt)
            # import pdb;pdb.set_trace()


        
            update = dbcon.execute("UPDATE `user_user` SET `password`='{}',`salt`='{}',`reset_password`=1 WHERE `email`='{}'".format(hashed,salt,email))
            if update : 

             
                subject = "Capital Biryani Password Reset"
                msg = "your updated password is :"+passwd
                user_email = get_user[0]["email"]
            
                try:
                    server = smtplib.SMTP('smtp.gmail.com:587')
                    server.ehlo()
                    server.starttls()
                    server.login("capitalbiryani2019@gmail.com", "capital@123")
                    message = 'Subject: {}\n\n{}'.format(subject, msg)
                    server.sendmail(user_email,user_email, message)
                    server.quit()
                    print("Success: Email sent!")
                    return Response({"data":True,"status":"01","message":"Success: Password sent to Registered emailid"}, status=200)
                except:
                    print("Email failed to send.")
                    return Response({"data":"ss","status":"01","message":"Fail"}, status=200)
            else : 
                return Response({"data":"ss","status":"01","message":"update faill"}, status=200)

        else :
            return Response({"data":"ss","status":"01","message":"email not found"}, status=200)



        

class UpdateUserFcm(APIView):

    def post(self, request):
        data = request.data
        id = data["id"]
        fcm_id = data["fcm_id"]
        get_user =  dbcon.execute("SELECT * FROM `user_user` WHERE `id`={}".format(id))
        # print(get_user)

        if get_user:
            
            update = dbcon.execute("UPDATE `user_user` SET `fcm_id` = '{}' WHERE `user_user`.`id` = {}".format(fcm_id,id))
            if update :
                get_user =  dbcon.execute("SELECT * FROM `user_user` WHERE `id`={}".format(id))

                
                return Response({"data":get_user,"status":"00","message":"success"}, status=200)
            else : 
                get_user =  dbcon.execute("SELECT * FROM `user_user` WHERE `id`={}".format(id))
                return Response({"data":get_user,"status":"01","message":"update faill"}, status=200)

        else :
            return Response({"data":"ss","status":"01","message":"user not found"}, status=200)





class UpdateVendorFcm(APIView):

    def post(self, request):
        data = request.data
        id = data["id"]
        fcm_id = data["fcm_id"]
        get_user =  dbcon.execute("SELECT * FROM `user_vendor` WHERE `id`={}".format(id))
        # print(get_user)

        if get_user:
            
            update = dbcon.execute("UPDATE `user_vendor` SET `fcm_id` = '{}' WHERE `user_vendor`.`id` = {}".format(fcm_id,id))
            if update :
                get_user =  dbcon.execute("SELECT * FROM `user_vendor` WHERE `id`={}".format(id))

                
                return Response({"data":get_user,"status":"00","message":"success"}, status=200)
            else : 
                get_user =  dbcon.execute("SELECT * FROM `user_vendor` WHERE `id`={}".format(id))
                return Response({"data":get_user,"status":"01","message":"update faill"}, status=200)

        else :
            return Response({"data":"ss","status":"01","message":"user not found"}, status=200)










    




