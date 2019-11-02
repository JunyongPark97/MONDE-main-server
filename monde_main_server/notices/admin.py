from django.contrib import admin
from notices.models import Notice, EventNotice, FAQ
from manage.sites import staff_panel


class HiddenNoticeAdmin(admin.ModelAdmin):
    list_display = ['key', 'title']


class BasePopupNoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'active', ]


class EventNoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', ]


class FAQNoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at', ]


class BaseNoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'important', 'hidden']


class TargetPopupNoticeReceiverAdmin(admin.ModelAdmin):
    list_display = ['id', '_notice_id', 'user', 'read_at']
    raw_id_fields = ['user', 'notice']

    def _notice_id(self, obj):
        return obj.notice_id


staff_panel.register(EventNotice, EventNoticeAdmin)
staff_panel.register(Notice, BaseNoticeAdmin)
staff_panel.register(FAQ, FAQNoticeAdmin)
