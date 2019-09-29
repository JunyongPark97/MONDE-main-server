# -*- encoding: utf-8 -*-
from django.contrib import admin

from categories.models import Shape, BagIllustration, Color, Handle, Deco, Charm, Pattern

admin.site.register(Shape)
admin.site.register(Color)
admin.site.register(Handle)
admin.site.register(Deco)
admin.site.register(Charm)
admin.site.register(Pattern)
admin.site.register(BagIllustration)

# class ShapeInline(admin.TabularInline):
#     model = BagIllustration
#
# @admin.register(Shape)
# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [
#         ShapeInline,]
