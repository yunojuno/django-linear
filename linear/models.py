from __future__ import annotations

from django.conf import settings
from django.db import models


class TShirtSizing(models.IntegerChoices):
    XS = 1, "👕"
    S = 2, "👕👕"
    M = 3, "👕👕👕"
    L = 5, "👕👕👕👕"
    XL = 8, "👕👕👕👕👕"


class LinearIssueManager(models.Manager):
    def from_json(self, issue_data: dict) -> LinearIssue:
        id = issue_data["id"]
        identifier = issue_data["identifier"]
        project = issue_data["project"] or {"milestone": None}
        milestone = project["milestone"] or {}
        team = issue_data["team"] or {}
        title = issue_data["title"]
        estimate = issue_data["estimate"]
        assignee = issue_data["assignee"] or {}
        state = issue_data["state"]
        return LinearIssue(
            id=id,
            identifier=identifier,
            team_name=team.get("name"),
            project_name=project.get("name", ""),
            milestone_name=milestone.get("name", ""),
            title=title,
            estimate=estimate,
            assignee_name=assignee.get("name", ""),
            state=state.get("name", ""),
        )

    def create_from_json(self, issue_data: dict) -> LinearIssue:
        issue = self.from_json(issue_data)
        issue.save()
        return issue


class LinearIssue(models.Model):
    """Representation of a Linear issue."""

    id = models.UUIDField(primary_key=True)
    identifier = models.CharField(max_length=10)
    team_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100, blank=True, default="")
    milestone_name = models.CharField(max_length=100, blank=True, default="")
    title = models.CharField(max_length=100, blank=True, default="")
    estimate = models.IntegerField(choices=TShirtSizing.choices, null=True)
    assignee_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    objects = LinearIssueManager()

    def __str__(self) -> str:
        return f"{self.identifier} - {self.title}"

    def get_absolute_url(self):
        """Returns the Linear issue URL."""
        workspace = getattr(settings, "LINEAR_WORKSPACE_NAME")
        return f"https://linear.app/{workspace}/issue/{self.identifier}"
