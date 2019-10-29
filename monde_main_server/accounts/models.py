from datetime import datetime

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from products.models import CrawlerProduct


class MondeUserManager(BaseUserManager):
    def create_user(self, uid, age):
        user = self.model(uid=uid)
        user.age = age
        user.save(using=self._db)
        return user

    def create_emailuser(self, email, password):
        user = self.model()
        user.is_superuser = False
        user.is_staff = False
        user.email = email
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_emailuser(
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        qs = super(MondeUserManager, self).get_queryset(*args, **kwargs)
        return qs


class MondeUser(AbstractBaseUser, PermissionsMixin):
    """
    user 입니다. 소셜로그인은 하지 않으며, 기기 uuid 로 로그인 및 유저 구별합니다.
    """
    objects = MondeUserManager()

    DEVICES = [
        (1, 'ANDROID'),
        (2, 'IOS'),
        (3, 'CHROME'),
    ]
    device_type = models.IntegerField(choices=DEVICES, null=True, blank=True)

    is_active = models.BooleanField(default=True, help_text="탈퇴할 경우 false로 변합니다.")
    is_banned = models.BooleanField(default=False)
    uid = models.UUIDField(default=None, blank=True, null=True, unique=True,
                           help_text="기기 id 입니다.")

    email = models.EmailField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False, help_text="super_user와의 권한 구분을 위해서 새로 만들었습니다. 일반적 운영진에게 부여됩니다.")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='수정한 날짜', db_index=True, null=True)

    nickname = models.CharField(max_length=120, verbose_name='닉네임', blank=True, null=True, unique=True)

    birth_year = models.PositiveIntegerField(blank=True, null=True, help_text="태어난 연도. 자동 계산됩니다.")
    age = models.PositiveIntegerField(blank=True, null=True, help_text="나이입니다.")

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.birth_year and self.age:
            self.birth_year = self.get_birth_year()
        super(MondeUser, self).save(*args, **kwargs)

    def is_admin(self):
        return self.is_staff

    def __str__(self):
        return str(self.uid)

    def __unicode__(self):
        return '{}] {}-{}'.format(self.id, self.device_type, self.uid)

    @property
    def social_default_nickname(self):
        if hasattr(self, 'common_profile'):
            return self.common_profile.nickname or self.common_profile.social_nickname or ''
        else:
            return ''

    def get_full_name(self):
        if self.social_default_nickname is not "":
            return '%s (%s)' % (self.social_default_nickname, self.__unicode__())
        return self.__unicode__()

    def get_short_name(self):
        return self.__unicode__()

    def get_birth_year(self):
        this_year = datetime.now().year
        birth_year = this_year + 1 - self.age
        return birth_year


class UserWithdrawalReason(models.Model):
    """
    사용자가 탈퇴를 하고자 할때 탈퇴에 대한 이유를 선택할 수 있도록 탈퇴 이유에 대한 모델.
    GET /api/v1/user/withdrawal_reason/
    """
    withdrawal_reason = models.CharField('탈퇴 이유', max_length=30, help_text='탈퇴 이유에 대한 설명입니다.')
    is_visible = models.BooleanField('활성화 여부', default=True)
    priority = models.IntegerField('우선순위', help_text='우선순위', default=-1)

    class Meta:
        verbose_name_plural = '회원 탈퇴 이유'

    def save(self, *args, **kwargs):
        if self.pk is None and self.priority == -1:
            withdrawal_reason = UserWithdrawalReason.objects.all().order_by('priority').last()
            if withdrawal_reason:
                self.priority = withdrawal_reason.priority + 1
            else:
                self.priority = 1

        super(UserWithdrawalReason, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{}] {}'.format(self.id, self.withdrawal_reason)


class DeleteUser(models.Model):
    """
    사용자가 탈퇴를 할때 탈퇴 이유에 대해 저장을 하는 모델.
    DELETE /api/v3/user/me/delete/
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='delete_user', on_delete=models.CASCADE)
    withdrawal_reasons = models.ManyToManyField(UserWithdrawalReason, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '탈퇴한 회원'