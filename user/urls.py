from django.urls import path,include
from user import views

urlpatterns = [
    path('users/', views.UserView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('addshippingaddress/', views.ShippingAddress.as_view()),
    path('getuseraddress/', views.UserAddress.as_view()),
    path('updateaddress/', views.UpdateAddress.as_view()),
    path('allvendors/', views.VendorsView.as_view()),
    path('updateprofile/', views.UpdateProfile.as_view()),
    path('deleteaddress/', views.DeleteAddress.as_view()),
    path('updatepassword/', views.UpdatePassword.as_view()),
    path('vendorlogin/', views.VendorLogin.as_view()),
    path('deliveryboy/', views.Deliveryboy.as_view()),
    path('deliveryboy/<int:id>/',views.DeliveryboyDetailsViews.as_view()),
    path('googlelogin/', views.GoogleLogin.as_view()),
    path('fogotpass/', views.FogotPass.as_view()),
    path('updateuserfcm/', views.UpdateUserFcm.as_view()),
    path('updatevendorfcm/', views.UpdateVendorFcm.as_view()),
    
]