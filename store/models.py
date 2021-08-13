from django.db.models.fields.related import ForeignKey
from django.urls.base import reverse
from category.models import Category
from django.db import models
from django.db.models.aggregates import Max
from category.models import Category
# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique= True)
    description = models.TextField(max_length=200, blank= True)
    price = models.IntegerField()
    images = models.ImageField(upload_to = 'photos/products')
    stock = models.IntegerField()
    is_availabel = models.BooleanField(default=True)
    # ForeignKey
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    variationfield = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def get_url(self):
        return reverse('product_detail', args= [self.category.slug, self.slug])

    def __str__ (self):
        return self.product_name

class VariationManger(models.Manager):
    def colors(self):
        return super(VariationManger, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManger, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
   
class Variation(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManger()
    def __str__(self):
        return self.variation_value