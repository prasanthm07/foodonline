from django.db import models
from accounts.models import User,UserProfile
from accounts.utlis import send_approved_mail

# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=20)
    vendor_lisence=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField( auto_now_add=True)

    def __str__(self) -> str:
        return self.vendor_name
    
    def save(self,*args, **kwargs):
        if self.pk is not None:
            orig=Vendor.objects.get(pk=self.pk)            
            if orig.is_approved!=self.is_approved:
                mail_template="accounts/emails/admin_is_approver.html"
                context={
                    'user':self.user,
                    'is_approved':self.is_approved
                }
                if self.is_approved==True: # 
                    mail_subject="congratulation your restaurant has been approved"
                    send_approved_mail(mail_subject,mail_template,context)
                else:
                    mail_subject="your restaurant not eligible please contanact support@foodonline.com"
                    send_approved_mail(mail_subject,mail_template,context)

        return super(Vendor,self).save(*args, **kwargs)