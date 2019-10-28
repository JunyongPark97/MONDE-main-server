from django.contrib import admin
from tools.sites import superadmin_panel
from ajax_select import make_ajax_form
import re
from django.core.exceptions import PermissionDenied
from django.contrib.admin.utils import label_for_field

# superadmin을 위한 helper function
from tools.steam_csv import StreamCSV


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


def export_as_csv(description="CSV file 저장",header=True):
    """
    This function returns an export csv action
    This function ONLY downloads the columns shown in the list_display of the admin
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/ and /2020/
        """
        # TODO Also create export_as_csv for exporting all columns including list_display
        if not request.user.is_staff:
            raise PermissionDenied
        opts = modeladmin.model._meta
        field_names = modeladmin.list_display
        if 'action_checkbox' in field_names:
            field_names.remove('action_checkbox')

        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        if header:
            headers = []
            for field_name in list(field_names):
                label = label_for_field(field_name,modeladmin.model,modeladmin)
                if type(label) != str:
                    label = str(label, 'utf-8')
                if str.islower(label):
                    label = str.title(label)
                headers.append(label)

        def data():
            for row in queryset:
                values = []
                for field in field_names:
                    try:
                        # Read from row
                        value = (getattr(row, field))
                        if callable(value):
                            try:
                                value = value() or ''
                            except:
                                value = 'Error retrieving value'
                        if value is None:
                            value = ''
                    except:
                        # Read by calling modeladmin method
                        value = (getattr(modeladmin, field))
                        if callable(value):
                            try:
                                value = value(row) or ''
                            except:
                                value = 'Error retrieving value'
                        if value is None:
                            value = ''
                        # Remove html tags, if exists
                        if type(value) == str:
                            value = str(value, 'utf-8')
                        elif hasattr(value, '__unicode__'):
                            value = value.__unicode__()
                        elif type(value) in [int]:
                            value = str(value)
                        value = re.sub(r'<.*?>', '', value)
                    values.append(str(value).encode('utf-8'))
                yield values

        my_csv = StreamCSV()
        my_csv.filename = 'filename=%s.csv' % str(opts).replace('.', '_')
        my_csv.heading = headers
        my_csv.data_generator = data()
        return my_csv.http_response()

    export_as_csv.short_description = description
    return export_as_csv
