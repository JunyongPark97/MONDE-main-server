from rest_framework import serializers

from products.models import CrawlerProduct
from search.category_search.models import CategorySearchRequest


class SearchResultListSerializer(serializers.ModelSerializer):
    pass


class CategorySearchRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    category_search_version = serializers.IntegerField(default=1)

    class Meta:
        model = CategorySearchRequest
        fields = ['user', 'categories', 'category_search_version']


class SampleListSerializer(serializers.ModelSerializer):
    on_sale = serializers.SerializerMethodField()
    color_tab = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CrawlerProduct
        fields = ['id',
                  'shopping_mall',
                  'product_name',
                  'bag_url',
                  'image_url',
                  'price',
                  'color_tab',
                  'on_sale']


    def get_image_url(self, product):
        image = product.bag_images.all().last()
        url = image.bag_image.url
        #TODO : Why bag_image.url isn't url?
        main_url = 'https://monde-web-crawler.s3.amazonaws.com/'
        added_url = main_url + url
        return added_url

    def get_color_tab(self, instance):
        tab_list = []
        for color_tab in instance.color_tabs.all():
            tab_list.append(color_tab.colors)
        return tab_list

    def get_colors(self, instance):
        color_list = []
        for color_tab in instance.color_tabs.all():
            #실제 판매중인 상품 색상명
            color_list.append(color_tab.colors)
        return color_list

    def get_on_sale(self, instance):
        sale_list = []
        for color_tab in instance.color_tabs.all():
            sale_list.append(color_tab.on_sale)
        if False in sale_list:
            return False
        return True


class CursorTestSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    cursor_next = serializers.SerializerMethodField()
    cursor_prev = serializers.SerializerMethodField()

    class Meta:
        model = CrawlerProduct
        fields = ['cursor_next', 'cursor_prev', 'data']

    def get_cursor_next(self, instance):
        paginated_response = self.context['paginated_response']
        return paginated_response['cursor-next']

    def get_cursor_prev(self, instance):
        paginated_response = self.context['paginated_response']
        return paginated_response['cursor-prev']

    def get_data(self, instance):
        serializer = SampleListSerializer(instance)
        return serializer.data