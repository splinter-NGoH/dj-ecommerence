from django.contrib import admin
from django.db import models
from .models import Products
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'is_availabel')
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Products, ProductAdmin)