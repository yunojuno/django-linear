from django.contrib import admin

from .models import LinearTask


@admin.register(LinearTask)
class LinearTaskAdmin(admin.ModelAdmin):
    list_display = (
        "identifier",
        "title",
        "milestone_name",
        "assignee_name",
        "estimate",
        "state",
    )
    list_filter = (
        "team_name",
        "state",
        "milestone_name",
        "assignee_name",
        "estimate",
        "project_name",
    )
    search_fields = ("project_name", "identifier")
