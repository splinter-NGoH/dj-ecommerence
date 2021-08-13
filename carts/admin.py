from django.contrib import admin
from .models import Cart,Cart_Item
# Register your models here.
class CartItemAdmin (admin.ModelAdmin):
    list_display = ['cart_id', 'date_field']
class CartAdmin (admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']
    list_editable = ['is_active',]
admin.site.register(Cart,CartItemAdmin)
admin.site.register(Cart_Item,CartAdmin)

