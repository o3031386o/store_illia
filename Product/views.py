import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import random


def homepage(request):
    subcategory = SubCategory.objects.filter(category__name="مردانه")
    products = Product.objects.all()
    recent = products[0:6] if products.count() >= 6 else products
    random_products = random.choices(products, k=(3 if products.count() >= 3 else products.count()))
    return render(request, template_name='index.html', context={'subcategory': subcategory,
                                                                'products': random_products,
                                                                'recent': recent})


def search(request):
    products = Product.objects.filter(name__icontains=request.GET['search'])
    color = Colors.objects.all()
    size = Size.objects.all()
    return render(request, template_name='searchpage.html', context={'products': products,
                                                                     'color': color,
                                                                     'size': size})


def product(request, pk):
    product = Product.objects.get(pk=pk)
    color = request.GET["color"]
    if color is not None:
        pass
    return render(request, template_name='product.html', context={'product': pk})


def product_filter_by_subcategory(request, pk):
    subcategory = SubCategory.objects.filter(category__name="مردانه")
    products = Product.objects.filter(sub_category__pk=pk)
    return render(request, template_name='product_filter_sub.html', context={'products': products,
                                                                             'subcategory': subcategory})










































































































































































































































def product_detail(request, pk):
    product_obj = get_object_or_404(Product, pk=pk)

    related_products = Product.objects.exclude(pk=pk)[:4]

    return render(request, "detail-page.html", {
        "product_obj": product_obj,
        "related_products": related_products
    })


@login_required
def cart_view(request):
    """نمایش سبد خرید کاربر"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})


@login_required
def add_to_cart(request, pk):
    """افزودن محصول به سبد خرید"""
    product_relation = get_object_or_404(SizeByColorProductRelations, pk=pk)

    # گرفتن سبد خرید یا ساختنش
    cart, created = Cart.objects.get_or_create(user=request.user)

    # بررسی اینکه محصول قبلاً تو سبد هست یا نه
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_relation=product_relation
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")


@login_required
def remove_from_cart(request, pk):
    """حذف کامل یک آیتم از سبد خرید"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
    cart_item.delete()
    return redirect("cart_view")


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})


def cart_detail(request):
    # گرفتن سبد خرید کاربر
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    total = cart.total_price
    return render(request, "cart.html", {"cart": cart, "items": items, "total": total})
