from django.http.response import HttpResponse
from carts.models import Cart_Item
from carts.views import _cart_id

from django.shortcuts import get_object_or_404, render
from .models import Products
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Products.objects.filter(category = categories, is_availabel = True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Products.objects.all().filter(is_availabel = True).order_by('created_date')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
        

    context = {
        'products': paged_products,
        'products_count': products_count,
        

    }
    return render(request, 'store/store.html', context)

def product_detail (request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug= category_slug, slug= product_slug)
        in_cart = Cart_Item.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search (request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Products.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)
