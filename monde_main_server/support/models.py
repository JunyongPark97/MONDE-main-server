from django.db import models
from django.conf import settings
from monde_main_server.settings import base
from ckeditor_uploader.fields import RichTextUploadingField
from versions.models import Version
from notices.tools import GiveRandomFileName

contact_upload_dir = GiveRandomFileName(path='support/contact')


class Official(models.Model):
    """
    이용약관, 개인정보처방침에 관한 모델입니다.
    """
    USE_TERM = 0
    PERSONAL_INFORMATION_USE_TERM = 1
    COMPANY_INFO = 2
    TYPES = (
        (USE_TERM, 'Use Term'),
        (PERSONAL_INFORMATION_USE_TERM, 'Personal Infromation Use Term'),
        (COMPANY_INFO, 'Company Introduce'),
    )
    official_type = models.IntegerField(choices=TYPES)
    version = models.IntegerField(default=0)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'[VER=%d] %s' % (self.version, self.get_official_type_display())

    class Meta:
        ordering = ['-version']


class MondeSupport(models.Model):
    """
    문의하기 모델입니다.
    """
    INQUIRY = 0
    SUGGEST = 1
    REPORT = 2
    OTEHRS = 10
    TYPES = (
        (INQUIRY, '문의'),
        (SUGGEST, '제안'),
        (REPORT, '오류신고'),
        (OTEHRS, '기타'),
    )

    user = models.ForeignKey(base.AUTH_USER_MODEL, related_name="supports", on_delete=models.CASCADE)
    contact_type = models.IntegerField(choices=TYPES)
    name = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    attached_file = models.ImageField(upload_to=contact_upload_dir, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
