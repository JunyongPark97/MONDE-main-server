from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from versions.models import Version


class FAQ(models.Model):
    """
    자주 묻는 질문/답변입니다.
    """
    title = models.CharField(max_length=40)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


# Loading message
def updateVersion():
    obj, created = Version.objects.get_or_create(
        name='loading_messages', defaults={'name': 'loading_messages'})
    if not created:
        obj.version += 1
        obj.save()


class LoadingMessage(models.Model):
    """
    앱을 시작할 때 하나씩 보여주는 loading message입니다.
    """
    title = models.CharField(max_length=40)
    user_type = models.IntegerField(default=0, help_text="all User")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "[%d]%s,만료일:%s" % (self.user_type, self.title, self.expired_at)

    def save(self):
        updateVersion()
        super(LoadingMessage, self).save()


class Official(models.Model):
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
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'[VER=%d] %s' % (self.version, self.get_official_type_display())

    class Meta:
        ordering = ['-version']


class MondeSupport(models.Model):
    CONTACT = 0

    contact_type = models.IntegerField(default=CONTACT)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    business_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
