from django.contrib import admin
from categories.models import Shape, BagIllustration, Color, Handle, Deco, Charm, Pattern


class CategoryInline(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'updated_at']


admin.site.register(Shape, CategoryInline)
admin.site.register(Color, CategoryInline)
admin.site.register(Handle, CategoryInline)
admin.site.register(Deco, CategoryInline)
admin.site.register(Charm, CategoryInline)
admin.site.register(Pattern, CategoryInline)
admin.site.register(BagIllustration)
