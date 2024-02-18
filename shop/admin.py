from django.contrib import admin
from .models import Product, Category
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('id', 'name', 'price', 'old_price',
                    'productImage', 'preview_text', 'created_at')

    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']