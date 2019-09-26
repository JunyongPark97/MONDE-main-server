from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from monde.models import Product, ProductImage, ProductCategories, ColorTab, Colors


class ProductAdmin(admin.ModelAdmin):
    list_display = ['shopping_mall', 'get_product_image_url', 'price', 'product_name']

    def get_product_image_url(self, bag):
        image = bag.image_url
        return mark_safe('<img src="%s" width=200px "/>' % image)


# admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductImage)
# admin.site.register(ProductCategories)
# admin.site.register(ColorTab)
# admin.site.register(Colors)

