from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Cart, Coupon, Order
from shop.models import Product

# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user,purchased=False)
    already_ordered = Order.objects.filter(user=request.user,ordered=False)
    
    if already_ordered.exists():
        order = already_ordered[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "this item quantity was updated.")
            return redirect('home')

        else:
            order.orderitems.add(order_item[0])
            messages.info(request, 'This item was added to your cart.')
            return redirect('home')
    else:
        order = Order(user = request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, 'This item was added to your cart.')
        return redirect('home')

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    # context = {'carts':carts, 'order':order}
    context = {'carts':carts}

    if orders.exists():
        if orders[0].coupon:
            context.update({
                'allredy_coupon': True
            })
        else:
            context.update({
                'allredy_coupon': False
            })
    coupon = Coupon.objects.all().order_by('-id')[0]
    if coupon.is_expaired == False:
        context.update({
            'coupon': coupon
        })
    

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(
            coupon_code=coupon_code, is_expaired=False)
        if coupon_obj.exists():
            if orders[0].get_totals() < coupon_obj[0].min_amount:
                messages.warning(
                    request, f'Your Amount is Low You Have to Shoping up to {coupon_obj[0].min_amount} tk !')
            else:

                order = orders[0]
                if order.coupon:

                    messages.info(request, 'You Got Already Discount !')
                else:
                    order.coupon = coupon_obj[0]
                    order.save()
                    messages.success(request, 'Coupon applied Successfully !')
                    return HttpResponseRedirect(reverse('App_order:cart'))
        else:
            messages.warning(request, 'Invalid Coupon !')

    if carts.exists() and orders.exists():
        context = {'order':order}
        order = orders[0]
        return render (request, 'order/cart.html', context=context)
    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect('home')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    already_ordered = Order.objects.filter(user=request.user, ordered=False)
    if already_ordered.exists():
        order = already_ordered[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was remove from your cart.")
            return redirect('cart')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('home')
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('home')
    

@login_required
def increase_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    already_ordered = Order.objects.filter(user=request.user, ordered=False)
    if already_ordered.exists():
        order = already_ordered[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} has been updated.")
                return redirect('cart')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('home')
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('home')

@login_required
def decrease_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    already_ordered = Order.objects.filter(user=request.user, ordered=False)
    if already_ordered.exists():
        order = already_ordered[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} has been updated.")
                return redirect('cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart")
                return redirect('home')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('home')
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('home')