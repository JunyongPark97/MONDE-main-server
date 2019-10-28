from django.contrib import admin
from categories.models import Shape, Color, Type, Pattern, TypeTag, Charm, Deco
from manage.sites import staff_panel


class CategoryInline(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'updated_at']


class TypeTagInline(admin.ModelAdmin):
    list_display = ['id', 'description']


class ByTypeInline(admin.ModelAdmin):
    list_display = ['id', 'detail', 'name', 'order', 'description', 'get_shape_tagname', 'active']

    @staticmethod
    def get_shape_tagname(shape):
        return shape.type.description


staff_panel.register(Shape, ByTypeInline)
staff_panel.register(Color, CategoryInline)
staff_panel.register(Type, CategoryInline)
staff_panel.register(TypeTag, TypeTagInline)
staff_panel.register(Deco, ByTypeInline)
staff_panel.register(Charm, ByTypeInline)
staff_panel.register(Pattern, CategoryInline)
# staff_panel.register(BagIllustration)
