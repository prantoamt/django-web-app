from django.shortcuts import render
from .models import Product as product
from .dict_key import dict_key

# Create your views here.

def products(request):
    products = product.objects.all()
    percentage_discount = {}
    for item in products:
        price = item.price
        sale = item.sale
        discount = price - sale
        percentage_discount[item.id] = int((discount/price)*100)
    template = 'products_template/home.html'
   
    context = {'products' : products,
                'percentage_discount' : percentage_discount}
    return render(request, template, context)

def single(request, slug):
    products = product.objects.get(slug=slug)
    template = 'products_template/single.html'
    context = {'product': products}
    return render(request, template, context)