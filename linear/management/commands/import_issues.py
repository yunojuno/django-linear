from __future__ import annotations

from typing import List

from django.core.management.base import BaseCommand

from linear.models import LinearIssue
from linear.queries import pull_issues


class Command(BaseCommand):
    help = "Import all issues from Linear"

    def handle(self, *args: object, **options: object) -> None:
        issues: List[LinearIssue] = []
        self.stdout.write("Fetching first page")
        _issues, page_info = pull_issues()
        issues += _issues
        while page_info["hasNextPage"]:
            after = str(page_info["endCursor"])
            self.stdout.write(f"Fetching next page: {after}")
            _issues, page_info = pull_issues(after=after, save=True)
            issues += _issues
        self.stdout.write(f"Total issues: {len(issues)}")
        for issue in issues:
            self.stdout.write(str(issue))
