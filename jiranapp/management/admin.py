from django.contrib import admin
from jiranapp.models import *

# Register your models here.
def post_notice(modeladmin, request, queryset):
    queryset.update(status='p')
post_notice.short_description = "Mark selected stories as published"


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'date']
    ordering = ['-date']
    actions = [post_notice]


admin.site.register(Notice, NoticeAdmin)