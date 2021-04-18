from django.contrib import admin
from .models import BotUser


def set_is_done(modeladmin, request, queryset):
    queryset.update(is_send=True)
set_is_done.short_description = "Mark selected as sent"

def unset_is_done(modeladmin, request, queryset):
    queryset.update(is_send=False)
unset_is_done.short_description = "Mark selected as not sent"


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'firstname', 
                    'lastname', 'created_at', 'updated_at')
    search_fields = ['user_id', 'firstname', 'lastname', 'username']
    list_filter = ('is_send', 'created_at', 'send_error')
    actions = [set_is_done, unset_is_done]


admin.site.register(BotUser, BotUserAdmin)