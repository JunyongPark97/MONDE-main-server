import jsonfield
from django.conf import settings
from django.db import models
from products.models import Bag
from search.category_search.models import CategorySearchResultLog
from shopping_malls.models import ShoppingMall
# Create your models here.


class ActivityItem(models.Model): #TODO : sync to web crawler db
    product_id = models.PositiveIntegerField(help_text="crwaling db에 저장된 product의 id를 저장합니다.")
    product_url = models.URLField()
    bag_images = jsonfield.JSONField(help_text="image url from S3 를 key=order, value=url로 저장합니다.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        Abstract = True


class UserFavoriteItem(ActivityItem): #TODO : ADD CATEGORY INFO
    is_hidden = models.BooleanField(default=False, help_text="사용자가 찜한 목록 삭제시 is_hidden=True")
    category_search_log = models.ForeignKey(CategorySearchResultLog, related_name="favorites", on_delete=models.SET_NULL ,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorite_items", on_delete=models.CASCADE)


class UserRecentlyViewItem(ActivityItem):
    is_hidden = models.BooleanField(default=False, help_text="사용자가 방문기록 삭제시 is_hidden=True")
    category_search_log = models.ForeignKey(CategorySearchResultLog, related_name="recently_views", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="recently_views", on_delete=models.CASCADE)


class UserFavoriteShop(models.Model):
    shop_id = models.PositiveIntegerField(help_text="web_crawling db에 있는 shopping number를 저장합니다 (ex: 1 = luzzibag)")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorite_shops", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False, help_text="사용자가 찜한 목록 삭제시")


class SearchHistory(models.Model):
    """
    CategorySearchRequest 로 대체 가능
    """
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    #
    # searched_item = models.ForeignKey(Bag, related_name="searched_histories", on_delete=models.CASCADE)
    # used_category = models.OneToOneField(UsedCategory, on_delete=models.CASCADE)
    pass

