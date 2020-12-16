from typing import List

from django.core.management.base import BaseCommand

from ...models import LinearTask
from ...queries import fetch_tasks


class Command(BaseCommand):
    help = "Import all tasks from Linear"

    def handle(self, *args, **options):
        tasks: List[LinearTask] = []
        self.stdout.write("Fetching first page")
        _tasks, page_info = fetch_tasks()
        tasks += _tasks
        while page_info["hasNextPage"]:
            after = page_info["endCursor"]
            self.stdout.write(f"Fetching next page: {after}")
            _tasks, page_info = fetch_tasks(after=after, save=True)
            tasks += _tasks
        self.stdout.write(f"Total issues: {len(tasks)}")
        for task in tasks:
            self.stdout.write(str(task))
