from django.contrib import admin

from api import models


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status',
        'created_at',
    )
    search_fields = (
        'title',
        'description',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
