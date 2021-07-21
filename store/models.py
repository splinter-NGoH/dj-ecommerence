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

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def get_url(self):
        return reverse('product_detail', args= [self.category.slug, self.slug])

    def __str__ (self):
        return self.product_name
