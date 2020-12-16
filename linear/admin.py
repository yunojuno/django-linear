from django.contrib import admin

from .models import LinearIssue


@admin.register(LinearIssue)
class LinearIssueAdmin(admin.ModelAdmin):
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
    readonly_fields = (
        "id",
        "team_name",
        "project_name",
        "identifier",
        "title",
        "milestone_name",
        "assignee_name",
        "estimate",
        "state",
    )
