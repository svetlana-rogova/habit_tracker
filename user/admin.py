from django.contrib import admin

from user.models import CustomUser


@admin.register(CustomUser)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'chat_id')
    search_fields = ('email',)

