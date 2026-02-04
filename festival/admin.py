from django.contrib import admin
from .models import Festival


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['address', 'begin_date', 'end_date']