from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from store.models import Products
# Create your models here.

class Cart (models.Model):
    cart_id = models.CharField(max_length= 250, blank=True)
    date_field = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.card_id




class Cart_Item (models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
        
    def __str__(self) -> str:
        return self.product