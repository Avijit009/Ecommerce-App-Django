from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Profile, Vendor
from .forms import ProfileForm, SignUpForm, VendorForm
# Create your views here.

def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully!")
            return HttpResponseRedirect(reverse('login'))
    return render(request,'account/signup.html', context={'form':form})

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    return render(request,'account/login.html', context = {'form':form})

@login_required
def log_out(request):
    logout(request)
    messages.warning(request, "You have been logged out!")
    return HttpResponseRedirect(reverse('home'))

@login_required
def user_profile(request):
    return render(request,'account/profile.html',)

@login_required
def update_profile(request):
    profile = Profile.objects.get(user = request.user)
    
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated!")
            form = ProfileForm(instance=profile)
    return render(request,'account/update_profile.html', context = {'form':form})

@login_required
def create_vendor(request):
    VendorProfile = Vendor.objects.filter(user=request.user)
    user_profile = Profile.objects.filter(user=request.user)
    form = VendorForm()
    if user_profile[0].is_fully_filled():
        if not VendorProfile:
            if request.method == 'POST':
                form = VendorForm(data=request.POST)
                if form.is_valid():
                    vendor_form = form.save(commit=False)
                    vendor_form.user = request.user
                    vendor_form.save()
                    messages.success(request, 'Congratulations ! You Are Our Vendor Now')
                    return HttpResponseRedirect(reverse('home'))
        else:
            messages.warning(request, 'You Already a Vendor !')
            return HttpResponseRedirect(reverse('home'))
    else:
        messages.warning(request, 'Please fillup Your Profile Information !')
        return HttpResponseRedirect(reverse('profile'))
    
    return render(request, 'account/vendor.html', context={'form': form})


@login_required
def password_change(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully !')
            return HttpResponseRedirect(reverse('App_shop:home'))
    return render(request, 'account/password_change.html', context={'form': form})