from django import forms
from .models import Vendor

class VendorFrom(forms.ModelForm):
    class Meta:
        model=Vendor
        fields=['vendor_name','vendor_lisence']