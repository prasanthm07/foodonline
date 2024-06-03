from django.urls import path,include
from .import views

urlpatterns = [
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myaccount/',views.myaccount,name='myaccount'),

    path('vendordashboard/',views.vendordashboard,name='vendordashboard'),
    path('cusdashboard/',views.cusdashboard,name='cusdashboard'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),

   
    path('forget_password/',views.forget_password,name='forget_password'),
    path('rest_password/<uidb64>/<token>/',views.reset_password_vaildate,name='rest_password_vaildate'),
    path('rest_password/',views.rest_password,name='rest_password'),

    path('vendor/',include('vendor.urls')),
]
