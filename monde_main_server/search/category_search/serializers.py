from rest_framework import serializers

from search.category_search.models import CategorySearchRequest


class SearchResultListSerializer(serializers.ModelSerializer):
    pass


class CategorySearchRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    category_search_version = serializers.IntegerField(default=1)

    class Meta:
        Model = CategorySearchRequest
        fields = ['user', 'categories', 'category_search_version']

