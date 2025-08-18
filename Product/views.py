import random

from django.shortcuts import render
from .models import *
import random

def homepage(request):
    subcategory = SubCategory.objects.filter(category__name="مردانه")
    products = Product.objects.all()
    recent = products[0:6] if products.count() >= 6 else products
    random_products = random.choices(products, k=(3 if products.count() >=3 else products.count()))
    return render(request,template_name='index.html', context={'subcategory': subcategory,
                                                               'products': random_products,
                                                               'recent': recent})

def search(request):
    products = Product.objects.filter(name__icontains=request.GET['search'])
    color = Colors.objects.all()
    size = Size.objects.all()
    return render(request,template_name='searchpage.html', context={'products': products,
                                                                    'color': color,
                                                                    'size': size})


def product(request,pk):
    product = Product.objects.get(pk=pk)
    color = request.GET["color"]
    if color is not None:
        pass
    return render(request,template_name='product.html', context={'product': pk})

