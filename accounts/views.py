from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserFrom
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorFrom
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.utlis import detectuser

# Create your views here.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):

    if request.user.is_authenticated:
        messages.warning(request,"you are already logined")
        return redirect('myaccount')
    
    elif request.method=='POST':
       
        form=UserFrom(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user= form.save(commit=False)
            user.set_password=(password)
            user.role= User.CUSTOMER
            print(user)
            user.save()
            messages.success(request,'your account been registered sucessfully')
            return redirect('registerUser')
        else:
            print(form.errors)
              
        
    else:
        form=UserFrom()
    context={
        'form':form,
    }

    
   
    
    return render(request,'accounts/registerUesr.html',context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"you are already logined")
        return redirect('myaccount')
    
    elif request.method=="POST":
        form=UserFrom(request.POST)
        V_form=VendorFrom(request.POST,request.FILES)
        
        if form.is_valid() and V_form.is_valid:
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.RESTAURNUT
            user.save()
            vendor=V_form.save(commit=False)
            vendor.user = user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,'your account been registered sucessfully')
            return redirect('registerVendor')
        else:
            print(form.errors)




    else:
        form=UserFrom()
        V_form=VendorFrom()
    context={
        'form':form,
        'V_form':V_form,
    }

    return render(request,'accounts/registerVendor.html',context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"you are already logined")
        return redirect('myaccount')
    
    elif request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,"your are logined")
            return redirect('myaccount')
        else:
            messages.error(request,"username or password is incorret")
            return redirect('login')


    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'you are logged out')
    return redirect('login')

@login_required(login_url='login')
def myaccount(request):
    user=request.user
    redirectUrl= detectuser(user)
    return redirect (redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request,'accounts/vendordashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cusdashboard(request):
    return render(request,'accounts/cusdashboard.html')
