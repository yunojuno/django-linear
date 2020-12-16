from __future__ import annotations

from typing import Any

from django.conf import settings
from django.db import models


class TShirtSizing(models.IntegerChoices):
    XS = 1, "👕"
    S = 2, "👕👕"
    M = 3, "👕👕👕"
    L = 5, "👕👕👕👕"
    XL = 8, "👕👕👕👕👕"


class LinearIssue(models.Model):
    """Representation of a Linear issue."""

    id = models.UUIDField(primary_key=True)
    identifier = models.CharField(max_length=10)
    team_name = models.CharField("team", max_length=100)
    project_name = models.CharField("project", max_length=100, blank=True, default="")
    milestone_name = models.CharField(
        "milestone", max_length=100, blank=True, default=""
    )
    title = models.CharField(max_length=100, blank=True, default="")
    estimate = models.IntegerField(choices=TShirtSizing.choices, null=True)
    assignee_name = models.CharField("assigned to", max_length=100)
    state = models.CharField(max_length=100)
    last_refreshed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "When this issue was last refreshed from Linear, via import or webhook"
        ),
    )

    class Meta:
        ordering = ["identifier"]
        permissions = [
            ("use_api", "Can run Linear API queries"),
        ]

    def __str__(self) -> str:
        return f"{self.identifier} - {self.title}"

    def get_absolute_url(self) -> str:
        """Return the Linear issue URL."""
        workspace = getattr(settings, "LINEAR_WORKSPACE_NAME")
        return f"https://linear.app/{workspace}/issue/{self.identifier}"

    def save(self, *args: Any, **kwargs: Any) -> LinearIssue:
        super().save(*args, **kwargs)
        return self
