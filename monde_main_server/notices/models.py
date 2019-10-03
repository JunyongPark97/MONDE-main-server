from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# from djrichtextfield.models import RichTextField
from django.db import models
from notices.tools import GiveRandomFileName

notice_upload_dir = GiveRandomFileName(path='uploads/event_notice')
news_upload_dir = GiveRandomFileName(path='uploads/news')
review_upload_dir = GiveRandomFileName(path='uploads/review')


class Notice(models.Model):
    """
    공지사항 모델입니다.
    """
    title = models.CharField(max_length=40, help_text="this field is title")
    content = RichTextUploadingField(help_text="rich_text_field로 이미지 등을 추가할 수 있습니다.")
    important = models.BooleanField(default=False, help_text="true일 경우 앱내 상단에 강조되어 표시됩니다.")
    hidden = models.BooleanField(default=False, help_text="true일 경우 공지 리스트에서 보이지 않습니다.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


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


class HiddenNotice(models.Model):
    """
    공지사항 리스트에 뜨지는 않지만 특정 행동시 같은 ui로 보여주는 팝업 등을 정의해놓은 모델입니다.
    """
    key = models.CharField(max_length=30)
    title = models.CharField(max_length=40)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class PopupNotice(models.Model):
    """
    앱 실행시 main화면에서 뜨는 popup입니다.
    """
    title = models.CharField(max_length=40)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    ios_visible = models.BooleanField(default=True)
    android_visible = models.BooleanField(default=True)


class EventNotice(models.Model):
    """
    이벤트 공지사항입니다. 이벤트 탭에 들어가면 banner가 보이고 클릭할 경우 공지사항처럼 content가 보입니다.
    """
    title = models.CharField(max_length=40)
    content = RichTextUploadingField()
    banner = models.ImageField(upload_to=notice_upload_dir)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class TargetPopupNotice(models.Model):
    """
    특정 사용자에게 팝업창을 띄울 때 사용하는 Notice 모델입니다.
    """
    title = models.CharField(max_length=40)
    content = RichTextUploadingField()
    key = models.CharField(max_length=100, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TargetPopupNoticeReceiver(models.Model):
    """
    팝업 대상과 읽음 여부를 저장하는 모델입니다.
    """
    # notice = models.ForeignKey(TargetPopupNotice, related_name='receivers')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='target_popup_notice_receivers')
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True,
                                   help_text='사용자가 팝업을 확인한 시간입니다.')
