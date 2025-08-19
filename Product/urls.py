from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from. views import*


urlpatterns = [
    path('',homepage),
    path('subcategory/<int:pk>', product_filter_by_subcategory, name='subcategory'),
    path('search/',search),
    path('product/<int:pk>/',product)
]


