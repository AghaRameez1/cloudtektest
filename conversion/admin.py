from django.contrib import admin

# Register your models here.
from conversion.models import DataTable


class DataTableAdmin(admin.ModelAdmin):
    list_display = ("name", "number","status")
admin.site.register(DataTable, DataTableAdmin)