from django.contrib import admin

from . import models


@admin.register(models.ObjectImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)