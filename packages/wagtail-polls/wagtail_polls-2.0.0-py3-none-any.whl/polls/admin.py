from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'ip']
    search_fields = ['user__username', 'item__message', 'ip']
