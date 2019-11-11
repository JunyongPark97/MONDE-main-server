from django.contrib import admin
from support.models import Official, MondeSupport
from manage.sites import staff_panel
from django.utils.safestring import mark_safe
from manage.pagination import FixedCountAdminPaginator


class MondeSupportAdmin(admin.ModelAdmin):
    list_per_page = 50
    paginator = FixedCountAdminPaginator
    list_display = ['contact_type', '_name', 'email', '_attached_file', 'created_at', 'is_answered']
    search_fields = ['name', 'email']
    list_filter = ['contact_type', 'is_answered']

    def _name(self, obj):
        if obj.name:
            return obj.name
        return None

    def _attached_file(self, obj):
        if obj.attached_file:
            url_name = obj.attached_file.name
            url = "https://monde-server-storages.s3.amazonaws.com/media/"
            url = url + url_name
            return mark_safe('<img src="%s" width=100px "/>' % url)
        return None


class OfficialAdmin(admin.ModelAdmin):
    list_display = ['official_type', 'version', 'updated_at']
    list_filter = ['official_type']


class TargetPopupNoticeReceiverAdmin(admin.ModelAdmin):
    list_display = ['id', '_notice_id', 'user', 'read_at']
    raw_id_fields = ['user', 'notice']

    def _notice_id(self, obj):
        return obj.notice_id


staff_panel.register(Official, OfficialAdmin)
staff_panel.register(MondeSupport, MondeSupportAdmin)
