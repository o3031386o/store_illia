from django.db import models

from Account.models import User


class Category(models.Model):
    name = models.CharField(max_length=56)
    icon = models.ImageField(upload_to='category_icon/')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=56)
    icon = models.ImageField(upload_to='subcategory_icon/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=56)
    descriptions = models.TextField()
    count = models.IntegerField(default=0)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Colors(models.Model):
    color_name = models.CharField(max_length=56)

    def __str__(self):
        return self.color_name


class Size(models.Model):
    size = models.CharField(max_length=56)

    def __str__(self):
        return f'{self.size}'


class ColorProductRelations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} : {self.color.color_name}'


class SizeByColorProductRelations(models.Model):
    color_product = models.ForeignKey(ColorProductRelations, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.color_product.product.name} : {self.color_product.color.color_name} : {self.size.size}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        counts = SizeByColorProductRelations.objects.filter(color_product__product=self.color_product.product)
        count = 0
        for i in counts:
            count += i.count
        self.color_product.product.count = count
        self.color_product.product.save()


class Gallery(models.Model):
    image = models.ImageField(upload_to='Gallery/')
    color_product = models.ForeignKey(ColorProductRelations, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.color_product.product.name} : {self.color_product.color.color_name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سبد خرید {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_relation = models.ForeignKey(SizeByColorProductRelations, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # اضافه کردن سایز و رنگ به نمایش
        size = self.product_relation.size  # فرض بر اینه که فیلد سایز همین اسم رو داره
        color = self.product_relation.color  # فرض بر اینه که فیلد رنگ همین اسم رو داره
        return f"{self.product_relation.product.name} - سایز: {size}, رنگ: {color} × {self.quantity}"

    @property
    def total_price(self):
        return self.product_relation.price * self.quantity
