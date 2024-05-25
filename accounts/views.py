from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserFrom
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method=='POST':
       
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