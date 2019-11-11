from django.contrib import admin
from notices.models import Notice, EventNotice, FAQ
from manage.sites import staff_panel


class FAQNoticeAdmin(admin.ModelAdmin):
    list_display = ['group', 'title', 'updated_at']
    list_filter = ['group']


class BaseNoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'important', 'hidden']


class TargetPopupNoticeReceiverAdmin(admin.ModelAdmin):
    list_display = ['id', '_notice_id', 'user', 'read_at']
    raw_id_fields = ['user', 'notice']

    def _notice_id(self, obj):
        return obj.notice_id


staff_panel.register(Notice, BaseNoticeAdmin)
staff_panel.register(FAQ, FAQNoticeAdmin)
