from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse


from order.models import Cart, Order
from .models import BillingAddress
from .forms import BillingAddressForm
from account.models import Profile


from sslcommerz_lib import SSLCOMMERZ 

# Create your views here.

@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    form = BillingAddressForm(instance=saved_address[0])
    if request.method == 'POST':
        form = BillingAddressForm(
            data=request.POST, instance=saved_address[0])
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.user = request.user
            user_form.save()
            form = BillingAddressForm(instance=saved_address[0])
            messages.success(request, 'Address Saved Successfully !')
            return redirect('checkout')

    return render(request, 'payment/checkout.html', context={'form': form, 'order_items': order_items, 'order_total': order_total})


@login_required
def payment(request):
    profile = Profile.objects.filter(user=request.user)[0]
    saved_address = BillingAddress.objects.filter(user=request.user)[0]

    if not profile.is_fully_filled():
        messages.warning(
            request, 'Please fill up all profile information first !')
        return redirect('profile')
    if not saved_address.is_fully_filled():
        messages.warning(request, 'Please fill up all  information first !')
        return redirect('checkout')

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_total = order_qs[0].get_totals()
    order_count = order_qs[0].orderitems.count()
    order_items = order_qs[0].orderitems.all()

    store_id = 'phoen6548b63b58096'
    API_key = 'phoen6548b63b58096@ssl'

    settings = {'store_id': store_id, 'store_pass': API_key, 'issandbox': True}
    sslcommez = SSLCOMMERZ(settings)

    status_url = request.build_absolute_uri(reverse('complete'))
    current_user = request.user

    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = profile.full_name
    post_body['cus_email'] = current_user.email
    post_body['cus_phone'] = profile.phone
    post_body['cus_add1'] = profile.address
    post_body['cus_city'] = profile.city
    post_body['cus_country'] = profile.country
    post_body['shipping_method'] = "Curiar"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = order_count
    post_body['product_name'] = order_items
    post_body['product_category'] = "Mixed"
    post_body['product_profile'] = "general"

    post_body['ship_name'] = profile.full_name
    post_body['ship_add1'] = saved_address.address
    post_body['ship_city'] = saved_address.city
    post_body['ship_postcode'] = saved_address.zipcode
    post_body['ship_country'] = saved_address.country

    response = sslcommez.createSession(post_body)
    return redirect(response['GatewayPageURL'])

@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,f"Your Payment Completed Successfully! Page will be redirected!")
            return HttpResponseRedirect(reverse("purchase", kwargs={'val_id':val_id, 'tran_id':tran_id},))
        elif status == 'FAILED':
            messages.warning(request, f"Your Payment Failed! Please Try Again! Page will be redirected!")

    return render(request, "payment/complete.html", context={})

@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    # orderId = tran_id
    # order.ordered = True
    # order.orderId = orderId
    # order.paymentId = val_id
    # orderId = tran_id
    order.ordered = True
    order.orderId = val_id
    order.paymentId = tran_id
    order.save()

    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("home"))

@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {"orders": orders}
    except:
        messages.warning(request, "You do no have an active order")
        return redirect("home")
    return render(request, "payment/order.html", context)
