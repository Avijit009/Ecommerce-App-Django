from django.urls import path

from . import views

urlpatterns = [
    path('',views.ProductView.as_view(), name='home'),
    path('product/<pk>/',views.ProductDetailsView.as_view(), name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('vendor_product/',views.view_sellar_product,name='vendor_product')
]