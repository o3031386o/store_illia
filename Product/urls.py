from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views
from. views import*


urlpatterns = [
    path('',homepage),
    path('subcategory/<int:pk>', product_filter_by_subcategory, name='subcategory'),
    path('search/',search),
    path('product/<int:pk>/', product),

    path('product_detail/<int:pk>/', views.product_detail, name="product_detail"),



    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_view, name="cart"),  # نمایش سبد خرید
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),  # اضافه کردن محصول
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_detail, name="cart_detail"),


]



