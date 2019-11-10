from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from monde.models import Product, ProductCategories
from manage.sites import staff_panel
from manage.pagination import FixedCountAdminPaginator
from django.utils.html import format_html
from django.db.models import Q


class CategoriesInline(admin.TabularInline):
    model = ProductCategories
    extra = 2  # 여분 작성 항목은 몇개를 기본으로 표시할 것인지


class ProductAdmin(admin.ModelAdmin):
    list_display = ['shopping_mall', 'get_product_image', 'price', 'name', 'get_categories', 'shop_product_url']
    list_per_page = 50
    paginator = FixedCountAdminPaginator
    inlines = [CategoriesInline]
    search_fields = ['categories__shape_result',
                     'categories__type_result',
                     'categories__charm_result',
                     'categories__pattern_result',
                     'categories__colors',]
    list_filter = ['shopping_mall']

    # TODO: FIX ME
    def get_search_results(self, request, queryset, search_term):
        print(search_term)
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_str = str(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(Q(categories__shape_result__icontains=search_term_as_str)|
                                                  Q(categories__type_result__icontains=search_term_as_str)|
                                                  Q(categories__charm_result__icontains=search_term_as_str)|
                                                  Q(categories__pattern_result__icontains=search_term_as_str)|
                                                  Q(categories__colors__icontains=search_term_as_str))
        return queryset, use_distinct

    @staticmethod
    def get_product_image(product):
        url = product.product_image_url
        return mark_safe('<img src="%s" width=200px "/>' % url)

    @staticmethod
    def get_categories(product):
        categories = product.categories
        return format_html(
            '<span>shape ..> {}</span> <br> <span>type .....> {}</span> <br>'
            '<span>charm ..> {}</span> <br> <span>pattern > {}</span> <br>'
            '<span>colors ..> {}</span>',
            list(categories.shape_result.keys()),
            list(categories.type_result.keys()),
            list(categories.charm_result.keys()),
            list(categories.pattern_result.keys()),
            list(categories.colors.keys()),
        )

    @staticmethod
    def shop_product_url(obj):
        return format_html("<a href='{url}'>상품으로 가기</a>", url=obj.product_url)

    shop_product_url.short_description = "Firm URL"


staff_panel.register(Product, ProductAdmin)


