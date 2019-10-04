from django.contrib import admin
from tools.manage.sites import staff_panel
from tools.manage.tools import superadmin_register
from notices.models import Notice,  HiddenNotice, EventNotice, FAQ


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


admin.site.register(EventNotice, EventNoticeAdmin)
admin.site.register(Notice, BaseNoticeAdmin)
admin.site.register(FAQ, FAQNoticeAdmin)
