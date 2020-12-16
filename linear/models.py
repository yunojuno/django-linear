from __future__ import annotations

from django.conf import settings
from django.db import models


class LinearTaskManager(models.Manager):
    def from_json(self, task_data: dict) -> LinearTask:
        id = task_data["id"]
        identifier = task_data["identifier"]
        project = task_data["project"] or {"milestone": None}
        milestone = project["milestone"] or {}
        team = task_data["team"] or {}
        title = task_data["title"]
        estimate = task_data["estimate"]
        assignee = task_data["assignee"] or {}
        state = task_data["state"]
        return LinearTask(
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

    def create_from_json(self, task_data: dict) -> LinearTask:
        task = self.from_json(task_data)
        task.save()
        return task


class LinearTask(models.Model):
    """Representation of a Linear task."""

    id = models.UUIDField(primary_key=True)
    identifier = models.CharField(max_length=10)
    team_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100, blank=True, default="")
    milestone_name = models.CharField(max_length=100, blank=True, default="")
    title = models.CharField(max_length=100, blank=True, default="")
    estimate = models.IntegerField(null=True)
    assignee_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    objects = LinearTaskManager()

    def __str__(self) -> str:
        return f"{self.identifier} - {self.title}"

    def get_absolute_url(self):
        """Returns the Linear task URL."""
        workspace = getattr(settings, "LINEAR_WORKSPACE_NAME")
        return f"https://linear.app/{workspace}/issue/{self.identifier}"
