from django.contrib import admin

from api import models

admin.site.site_title = 'ВШЭ'
admin.site.site_header = 'Администрирование общежитий ВШЭ'


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
    )


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'dormitory',
    )
    search_fields = (
        'user',
        'dormitory',
    )
    list_filter = (
        'dormitory',
    )


@admin.register(models.Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'main_text',
        'is_important',
        'created_at',
    )
    search_fields = (
        'main_text',
        'text',
    )
    list_filter = (
        'is_important',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
