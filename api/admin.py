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
        'problem',
        'dormitory',
        'is_read',
        'is_from_student',
        'created_at',
    )
    search_fields = (
        'text',
        'author',
        'problem',
    )
    list_filter = (
        'is_read',
        'is_from_student',
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


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'target_date',
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


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'dormitory',
        'is_login',
        'is_accept',
    )
    search_fields = (
        'user',
        'dormitory',
    )
    list_filter = (
        'dormitory',
        'is_login',
        'is_accept',
    )


@admin.register(models.Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'code',
    )
    search_fields = (
        'email',
        'code',
    )
