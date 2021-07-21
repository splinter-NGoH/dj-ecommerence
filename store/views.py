from django.shortcuts import get_object_or_404, render
from .models import Products
from category.models import Category
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Products.objects.filter(category = categories, is_availabel = True)
        products_count = products.count()
    else:
        products = Products.objects.all().filter(is_availabel = True)
        products_count = products.count()


    context = {
        'products': products,
        'products_count': products_count,

    }
    return render(request, 'store/store.html', context)

def product_detail (request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug= category_slug, slug= product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,

    }
    return render(request, 'store/product_detail.html', context)