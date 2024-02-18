from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile, Vendor

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        exclude = ['user']