from django.contrib import admin

from snippets.models import Snippets

@admin.register(Snippets)
class SnippetsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('first_name', 'last_name', 'adult','age')
    # list_filter =  ('adult')
    # ordering = ('first_name','last_name')
    list_per_page = 15
    date_hierarchy = 'created_at'