from django.conf import settings
from django.db import models
from products.models import Bag
from shopping_malls.models import ShoppingMall
# Create your models here.
class UserFavoriteItem(models.Model): #TODO : ADD CATEGORY INFO
    item = models.ForeignKey(Bag, related_name="favorited_lists", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorite_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False, help_text="사용자가 찜한 목록 삭제시")


class UserFavoriteShop(models.Model):
    shop = models.ForeignKey(ShoppingMall, related_name="favorited_lists", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorite_shops", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False, help_text="사용자가 찜한 목록 삭제시")


class UserRecentlyViewItem(models.Model): #TODO : ADD CATEGORY INFO
    item = models.ForeignKey(Bag, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="recently_viewed_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UsedCategory(models.Model):
    pass


class SearchHistory(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    searched_item = models.ForeignKey(Bag, related_name="searched_histories", on_delete=models.CASCADE)
    # used_category = models.OneToOneField(UsedCategory, on_delete=models.CASCADE)


