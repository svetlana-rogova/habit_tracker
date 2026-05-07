from django.contrib import admin

from tracker.models import Habit


@admin.register(Habit)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('owner', 'place', 'time', 'action', 'pleasant_habit', 'related_habit', 'periodicity', 'award',
                    'time_to_complete', 'is_public')
    search_fields = ('owner',)
