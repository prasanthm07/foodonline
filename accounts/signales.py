from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile

@receiver(post_save,sender=User)
def post_save_create_profile_view(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("profile was created")
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #create profule incase not there
            UserProfile.objects.create(user=instance)
            print("profile was not there so i created")
        print("user is updated")

@receiver(pre_save, sender=User)

def pre_save_profile_reciver(sender,instance, **kwargs):
   pass