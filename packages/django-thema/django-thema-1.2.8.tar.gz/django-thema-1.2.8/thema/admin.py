"""Admin configuration for the application thema."""

from django.contrib import admin

from thema.models import ThemaCategory


class ThemaCategoryAdmin(admin.ModelAdmin):
    """Class to manage admin for CategoryAdmin model."""

    list_display = [
        'code', 'header', 'parent', 'updated_at', 'notes',
    ]
    search_fields = ('code', 'parent__code', )


admin.site.register(ThemaCategory, ThemaCategoryAdmin)
