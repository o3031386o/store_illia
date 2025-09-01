import random
from django.core.paginator import Paginator
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


def product_filter_by_subcategory(request, pk):
    subcategory = SubCategory.objects.filter(category__name="مردانه")
    colors_filter = request.GET.getlist("colors", [])
    print(colors_filter)
    size_filter = request.GET.getlist("sizes", [])
    print(size_filter)



    sub_filter = SubCategory.objects.get(pk=pk)
    products = Product.objects.filter(sub_category = sub_filter)
    if size_filter != []:
        products = products.filter(colorproductrelations__sizebycolorproductrelations__size__size__in=size_filter)
    if colors_filter != []:
        products = products.filter(colorproductrelations__color__color_name__in=colors_filter)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name='product_filter_sub.html', context={'products': page_obj,
                                                                             'subcategory': subcategory})

