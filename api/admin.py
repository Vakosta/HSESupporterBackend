from django.contrib import admin

from api import models


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
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


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'is_read',
        'created_at',
    )
    search_fields = (
        'text',
        'author',
    )
    list_filter = (
        'is_read',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )


@admin.register(models.Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
    )
    search_fields = (
        'name',
        'address',
        'students',
    )
