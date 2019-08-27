from rest_framework import serializers

from search.category_search.models import CategorySearchRequest


class SearchResultListSerializer(serializers.ModelSerializer):
    pass


class CategorySearchRequestSerializer(serializers.ModelSerializer):

    class Meta:
        Model = CategorySearchRequest
        fields = ['categories']
