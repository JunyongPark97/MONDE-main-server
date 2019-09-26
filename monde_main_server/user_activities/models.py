from django.conf import settings
from django.db import models
from monde.models import Product
from products.models import CrawlerProduct


class UserProductViewLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recent_view_logs', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='user_view_logs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='수정한 날짜', db_index=True, null=True)
    is_hidden = models.BooleanField(default=False)
    count = models.IntegerField(default=1)


class UserProductFavoriteLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorite_logs', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='user_favorite_logs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='수정한 날짜', db_index=True, null=True)
    is_hidden = models.BooleanField(default=False)
    count = models.IntegerField(default=1)
