from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label',]
    list_per_page = 20
    search_fields = ['name__istartswith']
    