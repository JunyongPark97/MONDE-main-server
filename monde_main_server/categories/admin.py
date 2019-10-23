from django.contrib import admin
from categories.models import Shape, BagIllustration, Color, Type, Pattern, TypeTag, Charm, Deco


class CategoryInline(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'updated_at']


class TypeTagInline(admin.ModelAdmin):
    list_display = ['id', 'description']


class ByTypeInline(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'get_shape_tagname','active']

    @staticmethod
    def get_shape_tagname(shape):
        return shape.type.description


admin.site.register(Shape, ByTypeInline)
admin.site.register(Color, CategoryInline)
admin.site.register(Type, CategoryInline)
admin.site.register(TypeTag, TypeTagInline)
admin.site.register(Deco, ByTypeInline)
admin.site.register(Charm, ByTypeInline)
admin.site.register(Pattern, CategoryInline)
admin.site.register(BagIllustration)
