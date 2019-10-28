import datetime
import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MondeUserManager(BaseUserManager):
    def create_user(self,  uid):
        # if not username:
        #     raise ValueError('Users must have name.')
        user = self.model(uid=uid)
        # user.is_superuser = False
        # user.is_staff = False

        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, password):
        user = self.create_user(
            uid
            # password=password
        )
        # user.is_superuser = True
        # user.is_staff = True
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
    device_type = models.IntegerField(choices=DEVICES)

    is_active = models.BooleanField(default=True, help_text="탈퇴할 경우 false로 변합니다.")
    is_banned = models.BooleanField(default=False)
    uid = models.UUIDField(default=None, blank=True, null=True, unique=True,
                           help_text="기기 id 입니다.")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='수정한 날짜', db_index=True, null=True)

    nickname = models.CharField(max_length=120, verbose_name='닉네임', blank=True, null=True, unique=True)

    birth_year = models.DateField(blank=True, null=True, help_text="태어난 연도. 자동 계산됩니다.")
    age = models.PositiveIntegerField(blank=True, null=True, help_text="나이입니다.")

    USERNAME_FIELD = 'uid'

    def save(self, *args, **kwargs):
        if not self.birth_year:
            self.birth_year = self.get_birth_year()
        return super(MondeUser, self).save(*args, **kwargs)

    # def is_admin(self):
    #     return self.is_staff

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
        this_year = datetime.datetime.now().year
        birth_year = this_year + 1 - self.age
        return birth_year
