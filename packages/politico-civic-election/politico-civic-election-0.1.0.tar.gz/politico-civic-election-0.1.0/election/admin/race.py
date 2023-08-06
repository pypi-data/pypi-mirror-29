from django.contrib import admin


class RaceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['office']
    search_fields = ['label']
