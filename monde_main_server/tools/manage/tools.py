from django.contrib import admin
from tools.manage.sites import superadmin_panel
from ajax_select import make_ajax_form


# superadmin을 위한 helper function
def superadmin_register(model, user_fields=None, **kwargs):
    class ObjectAdmin(admin.ModelAdmin):
        pass
    if user_fields is not None:
        for user_field in user_fields:
            ObjectAdmin.form = make_ajax_form(model, {user_field: 'user_channel'})
    for key in kwargs:
        setattr(ObjectAdmin, key, kwargs[key])
    if 'list_display' in kwargs:
        list_display = kwargs['list_display']
        for col in list_display:
            # supports '_xx' notation for list_display
            if col[0] == '_':
                obj_attr = col[1:]
                list_method = (
                    lambda self, obj, obj_attr=obj_attr: getattr(obj, obj_attr))
                list_method.short_description = obj_attr
                setattr(ObjectAdmin, col, list_method)
    superadmin_panel.register(model, ObjectAdmin)