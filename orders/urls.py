from django.urls import path,include
from orders import views

urlpatterns = [
    path('addtocart/', views.AddToCartView.as_view()), 
    path('place/', views.OrderPlaceView.as_view()),
    path('cartdata/', views.CartDataView.as_view()),
    path('updatecart/', views.UpdateCartDataView.as_view()),
    path('deletecart/', views.DeleteCartDataView.as_view()),
    path('applycoupons/', views.ApplyCouponsView.as_view()),
    path('coupons/', views.CouponsView.as_view()),
    path('orderhistory/', views.OrderHistoryView.as_view()),
    path('acceptorder/', views.AcceptOrder.as_view()),
    path('assigndeliveryboy/', views.AssignDeliveryboy.as_view()),
    path('outfordeliovery/', views.Outfordeliovery.as_view()),
    path('deliverd/', views.Deliverd.as_view()),
    path('vendorwiseorders/', views.VendorWiseOrders.as_view()),
    path('ordersteps/', views.OrderSteps.as_view()),
    path('histrorybydate/', views.HistroryByDate.as_view()),
    path('cancelorder/', views.CancelOrder.as_view()),
    


    
]