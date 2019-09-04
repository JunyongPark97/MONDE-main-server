from django.db import models

# Create your models here.
from monde_main_server import settings


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