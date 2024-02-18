from django.db import models
from django.conf import settings

from account.models import Vendor

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='product_vendor')
    productImage = models.ImageField(upload_to='Products')
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    description = models.TextField(max_length=1000, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['created_at']