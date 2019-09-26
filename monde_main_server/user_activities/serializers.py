from rest_framework import serializers
from search.category_search.serializers import ProductResultSerializer
from user_activities.models import UserProductViewLogs, UserProductFavoriteLogs


# 상품 접속시 모델 저장 사용
class UserProductVisitLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProductViewLogs
        fields = ['user', 'product', 'is_hidden']


# 최근 검색 목록 보여줄때 사용
# DEPRECATED
class ProductRecentViewSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = UserProductViewLogs
        fields = ['product_detail']

    def get_product_detail(self, view_log):
        product = view_log.product
        serializer = ProductResultSerializer(product)
        return serializer.data


# 상품 찜할 때 모델 저장 사용
class UserProductFavoriteLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProductFavoriteLogs
        fields = ['user', 'product']


# 찜한 상품 목록 보여줄 때 사용
# DEPRECATED
class ProductFavoriteLogSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = UserProductFavoriteLogs
        fields = ['product_detail']

    def get_product_detail(self, favorite_log):
        product = favorite_log.product
        serializer = ProductResultSerializer(product)
        return serializer.data
