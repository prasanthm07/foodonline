from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings



def detectuser(user):
    if user.role==1:
        redirectUrl='vendordashboard'
        return redirectUrl
    elif user.role==2:
        redirectUrl='cusdashboard'
        return redirectUrl

    elif user.role == None and user.is_superadmin:
        redirectUrl ='/admin'
        return redirectUrl
    

def send_verfication_email(request,user,mail_subject,email_template):
    current_site=get_current_site(request)
    message=render_to_string(email_template,{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })    
    to_mail=user.email
    mail=EmailMessage(mail_subject,message,to=[to_mail])
    mail.send()

def send_approved_mail(mail_subject,mail_template,context):
    from_email=settings.DEFAULT_FROM_EMAIL
    message=render_to_string(mail_template,context)
    to_email=context['user'].email
    mail=EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()

    

 