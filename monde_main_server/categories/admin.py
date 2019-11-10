from django.contrib import admin
from categories.models import Shape, Color, Type, Pattern, TypeTag, Charm, Deco
from manage.sites import staff_panel
from django.utils.safestring import mark_safe


class TypeInline(admin.ModelAdmin):
    list_display = ['id', 'get_image', 'name', 'active', 'created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" width=330px "/>' % obj.image.url)


class TypeTagInline(admin.ModelAdmin):
    list_display = ['id', 'description']


class CharmInline(admin.ModelAdmin):
    list_display = ['id', 'get_image', 'name', 'active', 'created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" width=100px "/>' % obj.image.url)


class ShapeInline(admin.ModelAdmin):
    list_display = ['id', 'get_image', 'detail', 'name', 'order', 'description', 'get_shape_tagname', 'active']
    list_filter = ['type__description']

    @staticmethod
    def get_shape_tagname(shape):
        return shape.type.description

    def get_image(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" width=100px "/>' % obj.image.url)


class Color_PatternInline(admin.ModelAdmin):
    list_display = ['id', 'get_image', 'thumb_nail_image', 'get_selected_image', 'name', 'order', 'active']

    def thumb_nail_image(self, obj):
        if obj.thumb_nail:
            return mark_safe('<img src="%s" width=30px "/>' % obj.thumb_nail.url)

    def get_image(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" width=100px "/>' % obj.image.url)

    def get_selected_image(self, obj):
        if obj.selected_image:
            return mark_safe('<img src="%s" width=100px "/>' % obj.selected_image.url)



staff_panel.register(Shape, ShapeInline)
staff_panel.register(Charm, CharmInline)
staff_panel.register(Color, Color_PatternInline)
staff_panel.register(Pattern, Color_PatternInline)
staff_panel.register(Type, TypeInline)
staff_panel.register(TypeTag, TypeTagInline)
