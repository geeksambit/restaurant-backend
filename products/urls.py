from django.urls import path,include
from products import views

urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/<int:id>/',views.CategoryDetailsView.as_view()),
    path('cuisine/', views.CuisineView.as_view()),
    path('cuisine/<int:id>/',views.CuisineDetailsView.as_view()),
    path('products/', views.ProductsView.as_view()),
    path('products/<int:id>/',views.ProductDetailsViews.as_view()),
    path('productsbycuisine/<int:id>/',views.ProductCuisineViews.as_view()),
    path('productsbycategory/',views.ProductsByCategory.as_view()),
    path('allproductsbyvendor/',views.AllProductsByCategory.as_view()),
    path('allproductsbycusine/',views.AllProductsByCusine.as_view()),
    
]
