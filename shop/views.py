from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category
from account.models import Vendor
from .forms import ProductForm
# Create your views here.

class ProductView(ListView):
    model = Product
    template_name = 'shop/product_view.html'

class ProductDetailsView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'shop/product_details.html'

@login_required
def add_product(request):
    vendor = Vendor.objects.filter(user=request.user)[0]
    form = ProductForm()

    if vendor is not None and vendor.is_fully_filled():
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                add_product = form.save(commit=False)
                add_product.vendor = vendor
                add_product.save()
                messages.success(request, 'Product Added Successfully !')
    else:
        messages.success(request, 'Please fill up All Details')
        return HttpResponseRedirect(reverse('vendor'))

    return render(request, 'shop/add_product.html', context={'form': form})

@login_required
def view_vendor_product(request):
    vendor = Vendor.objects.filter(user=request.user)
    if vendor.exists():
        products = Product.objects.filter(vendor=vendor[0])
        if not products.exists():
            messages.warning(request,'You Have No Product !')
            return HttpResponseRedirect(reverse('home'))

    else:
        messages.warning(request, 'You Are Not Our Sellar !')
        return HttpResponseRedirect(reverse('App_shop:home'))

    return render(request, 'shop/vendor_product.html', context={'products':products})