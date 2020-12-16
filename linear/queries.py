from typing import Dict, List, Optional, Tuple, Union

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from linear.models import LinearIssue

PAGE_SIZE = getattr(settings, "LINEAR_API_PAGE_SIZE", 100)

ISSUES_QUERY = """
query ($pageSize: Int $after: String) {
  issues(first: $pageSize after: $after) {
      nodes {
        id
        identifier
        team{
          name
        }
        project{
          name
          milestone{
            name
          }
        }
        title
        estimate
        assignee{
          name
        }
        state{
          name
        }
    }
    pageInfo {
      startCursor
      endCursor
      hasNextPage
    }
  }
}
"""

PageInfoType = Dict[str, Union[str, bool]]
PagedIssuesResponseType = Tuple[List[LinearIssue], PageInfoType]


def fetch_issues(
    page_size: int = PAGE_SIZE, after: Optional[str] = None, save: bool = False
) -> PagedIssuesResponseType:
    if not settings.LINEAR_API_KEY:
        raise ImproperlyConfigured("LINEAR_API_KEY setting is missing")

    response = requests.post(
        url="https://api.linear.app/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": settings.LINEAR_API_KEY,
        },
        json={
            "query": ISSUES_QUERY,
            "variables": {"after": after, "pageSize": page_size},
        },
    )
    data = response.json()
    page_info = data["data"]["issues"]["pageInfo"]
    issues: List[LinearIssue] = []
    for issue in data["data"]["issues"]["nodes"]:
        if save:
            issue = LinearIssue.objects.create_from_json(issue)
        else:
            issue = LinearIssue.objects.from_json(issue)
        issues.append(issue)
    return issues, page_info
