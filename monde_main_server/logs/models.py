from django.db import models
from monde.models import Product
from monde_main_server.settings import base
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
    user = models.ForeignKey(base.AUTH_USER_MODEL, related_name='login_logs', null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=40, db_index=True)
    version = models.IntegerField(null=True, blank=True, db_index=True)
    # client_type = models.IntegerField(choices=CLIENT_TYPE, null=True, blank=True, db_index=True)
    # client_user_type = models.IntegerField(null=True, blank=True, db_index=True)
    # app_id = models.CharField(max_length=80, null=True, blank=True, db_index=True)
    # device = models.ForeignKey('accounts.DeviceInfo', related_name='login_logs', null=True, on_delete=models.SET_NULL)


class BannedUserLog(models.Model):
    """
    강제 퇴장당한 유저를 이유와 함께 기록합니다. / unset banned도 같이 기록
    """

    class Meta:
        verbose_name_plural = '사용제한(강퇴) 유저 로그'

    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    memo = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


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


class UserFeedback(models.Model):
    """
    검새 결과 피드백 저장 모델입니다.
    """
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedbacks")
    satisfaction = models.PositiveIntegerField(default=4)
    opinion = models.TextField(max_length=300, null=True, blank=True)
    search_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
