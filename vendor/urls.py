from django.urls import path,include
from .import views

urlpatterns = [

    path('vprofile/',views.vprofile,name='vprofile'),
    
]