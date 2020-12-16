from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from linear.queries import fetch_issue

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
        "created_at",
        "last_updated_at",
        "project_name",
    )
    search_fields = ("project_name", "identifier", "title")
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
        "created_at",
        "last_updated_at",
        "last_refreshed_at",
    )
    actions = ("sync_issue",)

    def sync_issue(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.count()
        for issue in queryset[:10]:
            update = fetch_issue(str(issue.id))
            self.message_user(
                request,
                f"Issue {update.identifier} was successfully updated.",
                messages.SUCCESS,
            )
        if count > 10:
            self.message_user(
                request,
                "Update ignored for remaining issues - use import command instead.",
                messages.WARNING,
            )
            return

    sync_issue.short_description = (  # type: ignore
        "Update selected linear issues via API"
    )
