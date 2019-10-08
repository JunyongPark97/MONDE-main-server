import uuid
from datetime import datetime, timedelta, time

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.utils import timezone

from products.models import CrawlerProduct
from tools.utils import create_random_string


class UserManager(BaseUserManager):
    def create_user(self,  username, password=None):
        # if not username:
        #     raise ValueError('Users must have name.')
        user = self.model(username=username)
        user.is_superuser = False
        user.is_staff = False

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        qs = super(UserManager, self).get_queryset(*args, **kwargs)
        return qs


# User models
class User(AbstractBaseUser, PermissionsMixin):
    """
        user입니다. django base user를 extends하여 만들었으며 3가지 가입 형태(이메일, 페이스북, 구글)에 따라서 구분합니다.
    """

    objects = UserManager()

    LOGIN_TYPE_EMAIL = 1
    LOGIN_TYPE_GOOGLE = 2
    LOGIN_TYPE_FACEBOOK = 3

    email = models.EmailField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="탈퇴할 경우 false로 변합니다.")
    is_staff = models.BooleanField(default=False, help_text="super_user와의 권한 구분을 위해서 새로 만들었습니다. 일반적 운영진에게 부여됩니다.")
    is_banned = models.BooleanField(default=False)
    uid = models.UUIDField(default=None, blank=True, null=True, unique=True,
                           help_text="email 대신 USERNAME_FIELD를 대체할 field입니다.")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='수정한 날짜', db_index=True, null=True)

    username = models.CharField(max_length=120, verbose_name='아이디', blank=True,null=True, unique=True)

    temporary_password = models.CharField(max_length=128, blank=True,
                                          help_text='원래 비밀번호와 다르게 임시로 사용할 수 있는 비밀번호입니다.')

    USERNAME_FIELD = 'username' # social login 시 uid 로 유저구분,

    def save(self, *args, **kwargs):
        if self.uid is None:
            self.uid = uuid.uuid4()
        return super(User, self).save(*args, **kwargs)

    def is_admin(self):
        return self.is_staff

    def __str__(self):
        return str(self.uid)

    def __unicode__(self):
        if self.email is not None:
            return '{id}] {mail}'.format(mail=self.email, id=self.id)
        return str(self.uid)

    @property
    def social_default_nickname(self):
        if hasattr(self, 'common_profile'):
            return self.common_profile.nickname or self.common_profile.social_nickname or ''
        else:
            return ''

    def get_home_name(self):
        if self.social_default_nickname != "":
            return self.social_default_nickname + ('name_suffix')
        else:
            return ('member')

    def get_full_name(self):
        if self.social_default_nickname is not "":
            return '%s (%s)' % (self.social_default_nickname, self.__unicode__())
        return self.__unicode__()

    def get_short_name(self):
        return self.__unicode__()


class CommonProfile(models.Model):

    GENDER = (
        (1, 'female'),
        (2, 'male'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='common_profile', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, null=True)
    social_nickname = models.CharField(max_length=40, help_text='social 계정 닉네임 (ex. google nickname)')
    gender = models.IntegerField(choices=GENDER, help_text="1=여자, 2=남자",
                                 blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True, help_text="나이대")

    def __unicode__(self):
        return self.user.__unicode__()


class DeviceInfo(models.Model):
    """
    device 정보를 저장하는 모델입니다.
    """
    DEVICES = [
        (1, 'ANDROID'),
        (2, 'IOS'),
        (3, 'CHROME'),
    ]
    device_type = models.IntegerField(choices=DEVICES)
    device_id = models.CharField(max_length=50, unique=True, db_index=True)

    def __unicode__(self):
        return '{}] {}-{}'.format(self.id, self.device_type, self.device_id)


class EmailVerificationStringManager(models.Manager):
    def create(self, **kwargs):
        random_string = create_random_string(8)
        kwargs.update(expire_at=timezone.now() + timedelta(hours=3), verification_string=random_string)
        return super(EmailVerificationStringManager, self).create(**kwargs)


class EmailVerificationString(models.Model):
    """
    email 인증을 위해 사용자에게 임시 인증 번호를 생성하고 저장하는 모델입니다.
    """
    email = models.CharField(max_length=255)
    verification_string = models.CharField(max_length=8)
    expire_at = models.DateTimeField()

    objects = EmailVerificationStringManager()

    def __unicode__(self):
        return '[{email}] {string}'.format(email=self.email, string=self.verification_string)
