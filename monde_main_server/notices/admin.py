# -*- encoding: utf-8 -*-
from django.contrib import admin
from tools.manage.sites import staff_panel
from tools.manage.tools import superadmin_register
from notices.models import (
    Notice,
    HiddenNotice, PopupNotice, EventNotice,
    TargetPopupNotice, TargetPopupNoticeReceiver)

# superadmin
superadmin_register(Notice, list_display=['id', 'title',])
superadmin_register(HiddenNotice, list_display=['id', 'title',])
superadmin_register(PopupNotice, list_display=['id', 'title',])
superadmin_register(EventNotice, list_display=['id', 'title',])


# staff
staff_panel.register(Notice)


class HiddenNoticeAdmin(admin.ModelAdmin):
    list_display = ['key', 'title']

class BasePopupNoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'active', ]

class EventNoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', ]

class IndexNewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link', 'created_at', ]

class TargetPopupNoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'title']

class TargetPopupNoticeReceiverAdmin(admin.ModelAdmin):
    list_display = ['id', '_notice_id', 'user', 'read_at']
    raw_id_fields = ['user', 'notice']

    def _notice_id(self, obj):
        return obj.notice_id

staff_panel.register(HiddenNotice, HiddenNoticeAdmin)
staff_panel.register(PopupNotice, BasePopupNoticeAdmin)
staff_panel.register(EventNotice, EventNoticeAdmin)
staff_panel.register(TargetPopupNotice, TargetPopupNoticeAdmin)
staff_panel.register(TargetPopupNoticeReceiver, TargetPopupNoticeReceiverAdmin)
