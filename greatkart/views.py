from store.models import Products
from django.shortcuts import render

def home (request):
    products = Products.objects.all().filter(is_availabel = True)
    context = {
        'products': products

    }
    return render (request, 'home.html', context)
