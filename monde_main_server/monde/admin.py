from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from monde.models import Product
from manage.sites import staff_panel
from manage.pagination import FixedCountAdminPaginator


class ProductAdmin(admin.ModelAdmin):
    list_display = ['shopping_mall', 'get_product_image', 'price', 'name', 'get_color_names', 'shop_url']
    list_per_page = 20
    paginator = FixedCountAdminPaginator

    @staticmethod
    def get_product_image(product):
        product_image = product.product_image
        if not product_image:
            return None
        url_tail = product_image.image.name
        main_url = 'https://monde-web-crawler.s3.amazonaws.com/'
        added_url = main_url + url_tail
        return mark_safe('<img src="%s" width=200px "/>' % added_url)

    @staticmethod
    def get_color_names(product):
        color_names = []
        for color_tab in product.color_tabs.all():
            # 실제 판매중인 상품 색상명
            color_names.append(color_tab.color_tab_name)
        return color_names

    @staticmethod
    def shop_url(obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.product_url)

    shop_url.short_description = "Firm URL"


staff_panel.register(Product, ProductAdmin)


