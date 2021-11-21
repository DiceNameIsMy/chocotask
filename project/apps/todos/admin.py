from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'priority', 'deadline', 'completed', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('priority', 'completed', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
