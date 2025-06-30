from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import (
    Category, SubCategory, Product, Colors, Size,
    ColorProductRelations, SizeByColorProductRelations, Gallery
)


class SizeByColorProductRelationsInline(admin.TabularInline):
    model = SizeByColorProductRelations
    extra = 0
    min_num = 1
    autocomplete_fields = ['size']
    fields = ('size', 'count')


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    fields = ('image', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'تصویر پیش‌نمایش'


@admin.register(ColorProductRelations)
class ColorProductRelationsAdmin(admin.ModelAdmin):
    list_display = ('product','color', 'total_count', )
    search_fields = ['product__name', 'color__color_name']
    list_filter = ['color']
    autocomplete_fields = ['product', 'color']
    inlines = [SizeByColorProductRelationsInline, GalleryInline]
    readonly_fields = ['total_count']

    # def product_link(self, obj):
    #     url = reverse('admin:app_product_change', args=[obj.product.id])
    #     return format_html('<a href="{}">{}</a>', url, obj.product.name)
    # product_link.short_description = "محصول"
    # product_link.admin_order_field = 'product__name'

    def total_count(self, obj):
        total = SizeByColorProductRelations.objects.filter(color_product=obj).aggregate(
            total=Sum('count')
        )['total'] or 0
        return total
    total_count.short_description = "مجموع موجودی"

    # def view_gallery(self, obj):
    #     count = obj.gallery_set.count()
    #     url = reverse('admin:app_gallery_changelist') + '?' + urlencode({'color_product__id': str(obj.id)})
    #     return format_html('<a href="{}">{} تصویر</a>', url, count)
    # view_gallery.short_description = "گالری تصاویر"


@admin.action(description='ریست کردن موجودی محصول')
def reset_product_count(modeladmin, request, queryset):
    for product in queryset:
        product.count = 0
        product.save()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'related_color_count', 'sub_category')
    search_fields = ['name']
    actions = [reset_product_count]
    autocomplete_fields = ['sub_category']

    def related_color_count(self, obj):
        return obj.colorproductrelations_set.count()
    related_color_count.short_description = "تعداد رنگ‌ها"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']
    autocomplete_fields = ['category']


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = ['color_name']
    search_fields = ['color_name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    search_fields = ['size']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = ['color_product', 'image', 'thumbnail']
    search_fields = ['color_product__product__name', 'color_product__color__color_name']
    readonly_fields = ['thumbnail']
    autocomplete_fields = ['color_product']

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'تصویر پیش‌نمایش'
