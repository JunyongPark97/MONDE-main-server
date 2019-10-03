from rest_framework import serializers
from monde.models import Product
from products.models import CrawlerProduct
from search.category_search.models import CategorySearchRequest


class CategorySearchRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_search_version = serializers.IntegerField(default=1)

    class Meta:
        model = CategorySearchRequest
        fields = ['user', 'categories', 'category_search_version', 'created_at']


class ProductResultSerializer(serializers.ModelSerializer):
    """
    검색 또는 필터링 된 product 를 list 형태로 보여주기 위한 serializer 입니다.
    """
    image_url = serializers.SerializerMethodField()
    color_names = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'is_favorite',
                  'product_url',
                  'image_url',
                  'price',
                  'is_on_sale',
                  'color_names',
                  'colors',
                  'view_count']


    def get_is_favorite(self, instance):
        user = self.context['request'].user
        favorite_log = instance.user_favorite_logs.filter(user=user).last()
        if not favorite_log:
            return None
        if favorite_log.is_hidden:
            return False
        return True

    def get_image_url(self, product):
        product_image = product.product_image
        if not product_image:
            return None
        url_tail = product_image.image.name
        # TODO : Why bag_image.url isn't url?
        main_url = 'https://monde-web-crawler.s3.amazonaws.com/'
        added_url = main_url + url_tail
        return added_url

    def get_color_names(self, instance):
        color_names = []
        for color_tab in instance.color_tabs.all():
            # 실제 판매중인 상품 색상명
            color_names.append(color_tab.color_tab_name)
        return color_names

    def get_colors(self, instance):
        color_list = []
        for color_tab in instance.color_tabs.all():
            #TODO : 유효성 검증 필요
            colors = color_tab.colors.all()
            for color in colors:
                color_list.append(color.color)
        return color_list

    # Temp
    def get_view_count(self, instance):
        try:
            views = instance.view_count
            return views.view_count
        except:
            pass
        return None


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
