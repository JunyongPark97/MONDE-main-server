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
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    colors = serializers.SerializerMethodField()
    on_sale = serializers.SerializerMethodField()
    color_tab = serializers.SerializerMethodField()

    class Meta:
        model = CrawlerProduct
        fields = ['id','shopping_mall', 'image_url', 'product_name','bag_url','price','color_tab', 'colors', 'on_sale']


    def get_color_tab(self, instance):
        tab_list = []
        for color_tab in instance.color_tabs.all():
            tab_list.append(color_tab.colors)
        return tab_list

    def get_colors(self, instance):
        color_list=[]
        for color_tab in instance.color_tabs.all():
            for color in color_tab.color_tags.all():
                color_list.append(color.color)
        return color_list

    def get_on_sale(self, instance):
        sale_list = []
        for color_tab in instance.color_tabs.all():
            print(color_tab.on_sale)
            sale_list.append(color_tab.on_sale)
        if False in sale_list:
            return False
        return True

