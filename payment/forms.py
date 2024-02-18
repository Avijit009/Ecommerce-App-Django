from django import forms

from .models import BillingAddress

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ['user']