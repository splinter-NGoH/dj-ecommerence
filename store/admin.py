from django.contrib import admin
from django.db import models
from .models import Products, Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'is_availabel')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdimn (admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'created_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'created_date', 'is_active')
admin.site.register(Products, ProductAdmin)
admin.site.register(Variation, VariationAdimn)