from django.contrib import admin
from categories.models import Shape, BagIllustration, Color, Type, CharmDeco, Pattern, TypeTag


class CategoryInline(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'updated_at']


class TypeTagInline(admin.ModelAdmin):
    list_display = ['id', 'description']


class ShapeInline(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'active']


admin.site.register(Shape, ShapeInline)
admin.site.register(Color, CategoryInline)
admin.site.register(Type, CategoryInline)
admin.site.register(TypeTag, TypeTagInline)
# admin.site.register(Deco, CategoryInline)
admin.site.register(CharmDeco, CategoryInline)
admin.site.register(Pattern, CategoryInline)
admin.site.register(BagIllustration)
