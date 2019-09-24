from rest_framework import serializers

from user_activities.models import UserProductViewLogs, UserProductFavoriteLogs
from products.models import CrawlerProduct


class ProductVisitLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.SerializerMethodField()
    shopping_mall = serializers.SerializerMethodField()
    bag_url = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = UserProductViewLogs
        fields = '__all__'


class ProductRecentViewSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = UserProductViewLogs
        fields = ('id', 'product_id', 'favorite', 'created_at', 'product_name',
                  'bag_url', 'price', 'colors', 'image_url')

    def get_favorite(self, instance):
        user = self.context['request'].user
        product_id = instance.product_id
        favorite_log = UserProductFavoriteLogs.objects.filter(product_id=product_id, user=user).last()
        if not favorite_log:
            return False
        if favorite_log.is_hidden:
            return False
        return True

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


class ProductFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.SerializerMethodField()
    shopping_mall = serializers.SerializerMethodField()
    bag_url = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = UserProductFavoriteLogs
        fields = '__all__'


class ProductFavoriteLogSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = UserProductFavoriteLogs
        fields = ('id', 'product_id', 'favorite', 'created_at', 'product_name',
                  'bag_url', 'price', 'colors', 'image_url')

    def get_favorite(self, instance):
        if instance.is_hidden:
            return False
        return True

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
