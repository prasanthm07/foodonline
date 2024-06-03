from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserFrom
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorFrom
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.utlis import detectuser,send_verfication_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor


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
            print("done")
            send_verfication_email(request,user)
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
            print("done")
            mail_subject="please activate your account"
            mail_template='accounts/emails/account_verificaton.html'

            send_verfication_email(request,user,mail_subject,mail_template)
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


def activate(request,uidb64,token):
    #active the user by setting the is_actvate status to true
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"congratulation your account is activated")
        return redirect('myaccount')
    else:
        messages.error(request,'Invaild activation link')
        return redirect('myaccount')


    
    


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

@login_required(login_url='login')# set the custome or vendor
def myaccount(request):
    user=request.user
    redirectUrl= detectuser(user)
    return redirect (redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    
    return render(request,'accounts/vendordashboard.html',)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cusdashboard(request):
    return render(request,'accounts/cusdashboard.html')

def forget_password(request):
    if request.method=='POST':
        email=request.POST['email']

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            mail_subject="please activate your account"
            mail_template='accounts/emails/resetpassword.html'

            send_verfication_email(request,user,mail_subject,mail_template)
            messages.success(request,'password reset link has been sent your email address')
            return redirect('rest_password')
        else:
            messages.error(request,'Account does not exit')
            return redirect('forget_password')
        
    return render(request,'accounts/forget_password.html')

def reset_password_vaildate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'please reset your password')
        return redirect ('rest_password')
    else:
        messages.error(request,'link has been expried')
   
   

def rest_password(request):
   if request.method=='POST':
       password=request.POST['password']
       confirm_password=request.POST['confirm_password']

       if password==confirm_password:
           pk=request.session.get('uid')
           user=User.objects.get(pk=pk)
           user.set_password(password)
           user.is_active=True
           user.save()

       else:
            messages.error(request,'password reset sucessfully')
            return redirect('reset_password')
           
          
   return render(request,'accounts/reset_password.html')

