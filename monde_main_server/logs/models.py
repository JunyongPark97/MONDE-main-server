from django.db import models
from monde.models import Product
from monde_main_server import settings
from products.models import CrawlerProduct


class LoginLog(models.Model):

    class Meta:
        verbose_name_plural = '로그인 로그'

    ANDROID = 1
    IOS = 2
    WEB = 3
    ETC = 4

    CLIENT_TYPE = (
        (ANDROID, 'android'),
        (IOS, 'ios'),
        (WEB, 'web'),
        (ETC, 'etc'),
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='login_logs', null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=40, db_index=True)
    version = models.IntegerField(null=True, blank=True, db_index=True)
    client_type = models.IntegerField(choices=CLIENT_TYPE, null=True, blank=True, db_index=True)
    client_user_type = models.IntegerField(null=True, blank=True, db_index=True)
    app_id = models.CharField(max_length=80, null=True, blank=True, db_index=True)
    device = models.ForeignKey('accounts.DeviceInfo', related_name='login_logs', null=True, on_delete=models.SET_NULL)


# product view log
class ProductViewCount(models.Model):
    product = models.OneToOneField(Product, related_name='view_count', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=1)
    description = models.CharField(max_length=500)


# product favorite log
class ProductFavoriteCount(models.Model):
    product = models.OneToOneField(Product, related_name='favorite_count', on_delete=models.CASCADE)
    favorite_count = models.IntegerField(default=1)
    description = models.CharField(max_length=500)


# db sync log
class DBProductSyncLogs(models.Model):
    db_product_id = models.IntegerField()
    cause = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DBProductImageSyncLogs(models.Model):
    db_product_image_id = models.IntegerField()
    cause = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DBCategorySyncLogs(models.Model):
    db_category_id = models.IntegerField()
    cause = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DBColorTabSyncLogs(models.Model):
    db_colortab_id = models.IntegerField()
    cause = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DBColorSyncLogs(models.Model):
    db_color_id = models.IntegerField()
    cause = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
