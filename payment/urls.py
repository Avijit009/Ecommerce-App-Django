from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.payment, name='payment'),
    path('complete/', views.complete, name='complete'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name="purchase"),
    path('order/', views.order_view, name="order"),
]