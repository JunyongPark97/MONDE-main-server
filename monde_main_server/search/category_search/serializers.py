from rest_framework import serializers

from user_activities.models import ProductViewLogs
from products.models import CrawlerProduct
from search.category_search.models import CategorySearchRequest


class SearchResultListSerializer(serializers.ModelSerializer):
    pass


class CategorySearchRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_search_version = serializers.IntegerField(default=1)

    class Meta:
        model = CategorySearchRequest
        fields = ['user', 'categories', 'category_search_version', 'created_at']


class ProductResultSerializer(serializers.ModelSerializer):
    """
    category search result 를 list 형태로 보여주기 위한 serializer 입니다.
    """
    on_sale = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()

    class Meta:
        model = CrawlerProduct
        fields = ['id',
                  'product_name',
                  'bag_url',
                  'image_url',
                  'price',
                  'on_sale',
                  'colors']

    def get_image_url(self, product):
        image = product.bag_images.all().last()
        url = image.bag_image.url
        # TODO : Why bag_image.url isn't url?
        main_url = 'https://monde-web-crawler.s3.amazonaws.com/'
        added_url = main_url + url
        return added_url

    def get_colors(self, instance):
        color_list = []
        for color_tab in instance.color_tabs.all():
            # 실제 판매중인 상품 색상명
            color_list.append(color_tab.colors)
        return color_list

    def get_on_sale(self, instance):
        sale_list = []
        for color_tab in instance.color_tabs.all():
            sale_list.append(color_tab.on_sale)
        if False in sale_list:
            return False
        return True


class ProductVisitLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.SerializerMethodField()
    shopping_mall = serializers.SerializerMethodField()
    bag_url = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductViewLogs
        fields = '__all__'


class ProductRecentViewSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductViewLogs
        fields = ('id', 'product_id', 'created_at', 'product_name',
                  'bag_url', 'price', 'colors', 'image_url')

    def get_colors(self, instance):
        product_id = instance.product_id
        product = CrawlerProduct.objects.filter(pk=product_id).last()
        color_list = []
        for color_tab in product.color_tabs.all():
            # 실제 판매중인 상품 색상명
            color_list.append(color_tab.colors)
        return color_list

    def get_image_url(self, instance):
        product_id = instance.product_id
        product = CrawlerProduct.objects.filter(pk=product_id).last()
        image = product.bag_images.all().last()
        if not image:
            return None
        url = image.bag_image.url
        # TODO : Why bag_image.url isn't url?
        main_url = 'https://monde-web-crawler.s3.amazonaws.com/'
        added_url = main_url + url
        return added_url


class SampleListSerializer(serializers.ModelSerializer):
    on_sale = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    category_data = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()

    class Meta:
        model = CrawlerProduct
        fields = ['id',
                  'category_data',
                  'product_name',
                  'bag_url',
                  'image_url',
                  'price',
                  'on_sale',
                  'colors']

    def get_category_data(self, product):
        bag_image = product.bag_images.first()
        category = bag_image.categories
        data = {}
        data['shape'] = category.shape_result
        data['handle'] = category.handle_result
        data['color'] = category.color_result
        data['charm'] = category.charm_result
        data['deco'] = category.deco_result
        data['pattern'] = category.pattern_result
        return data

    def get_image_url(self, product):
        image = product.bag_images.all().last()
        url = image.bag_image.url
        #TODO : Why bag_image.url isn't url?
        main_url = 'https://monde-web-crawler.s3.amazonaws.com/'
        added_url = main_url + url
        return added_url

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