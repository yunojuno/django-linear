"""GraphQL API query functions."""
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now as tz_now

from linear.models import LinearIssue

PAGE_SIZE = getattr(settings, "LINEAR_API_PAGE_SIZE", 100)

QueryResponseType = Dict[str, Any]
PageInfoType = Dict[str, Union[str, bool]]
PagedIssuesResponseType = Tuple[List[LinearIssue], PageInfoType]


class LinearApiError(Exception):
    pass


def parse_issue_node(issue_data: dict) -> LinearIssue:
    """Parse GraphQL response node into a new LinearIssue object (unsaved)."""
    id = issue_data["id"]
    identifier = issue_data["identifier"]
    project = issue_data["project"] or {"milestone": None}
    milestone = project["milestone"] or {}
    team = issue_data["team"] or {}
    title = issue_data["title"]
    estimate = issue_data["estimate"]
    assignee = issue_data["assignee"] or {}
    state = issue_data["state"]
    created_at = issue_data["createdAt"]
    last_updated_at = issue_data["updatedAt"]
    return LinearIssue(
        id=id,
        identifier=identifier,
        team_name=team.get("name"),
        project_name=project.get("name", ""),
        milestone_name=milestone.get("name", ""),
        title=title[:100],
        estimate=estimate,
        assignee_name=assignee.get("name", ""),
        state=state.get("name", ""),
        created_at=created_at,
        last_updated_at=last_updated_at,
    )


def run_query(query: str, **variables: Any) -> QueryResponseType:
    """Run GraphQL query and return the "data" contents."""
    if not settings.LINEAR_API_KEY:
        raise ImproperlyConfigured("LINEAR_API_KEY setting is missing")

    response = requests.post(
        url="https://api.linear.app/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": settings.LINEAR_API_KEY,
        },
        json={
            "query": query,
            "variables": variables,
        },
    )
    payload = response.json()
    if "errors" in payload:
        msg = "; ".join([e["message"] for e in payload["errors"]])
        raise LinearApiError(msg)
    return payload["data"]


def fetch_issues(
    page_size: int = PAGE_SIZE, after: Optional[str] = None, save: bool = False
) -> PagedIssuesResponseType:
    """Fetch a page of issues from the API, without saving them."""
    query = """
      query ($pageSize: Int $after: String) {
        issues(first: $pageSize after: $after) {
          nodes {
            id
            identifier
            team {
              name
            }
            project {
              name
              milestone {
                name
              }
            }
            title
            estimate
            assignee {
              name
            }
            state {
              name
            }
            createdAt
            updatedAt
          }
          pageInfo {
            startCursor
            endCursor
            hasNextPage
          }
        }
      }
    """
    data = run_query(query, after=after, pageSize=page_size)
    page_info = data["issues"]["pageInfo"]
    issues: List[LinearIssue] = []
    for node in data["issues"]["nodes"]:
        issue = parse_issue_node(node)
        issue.last_refreshed_at = tz_now()
        issues.append(issue)
    return issues, page_info


def pull_issues(
    page_size: int = PAGE_SIZE, after: Optional[str] = None, save: bool = False
) -> PagedIssuesResponseType:
    """Fetch a page of issues from the API and save them locally."""
    issues, page_info = fetch_issues(page_size=page_size, after=after)
    for issue in issues:
        issue.save()
    return issues, page_info


def fetch_issue(id: str) -> LinearIssue:
    """Fetch an issue by id from the Linear API, without saving."""
    query = """
      query ($id: String!) {
        issue(id: $id) {
          id
          identifier
          team{name}
          project{name milestone{name}}
          title
          estimate
          assignee{name}
          state{name}
        }
      }
    """
    data = run_query(query, id=id)
    issue = parse_issue_node(data["issue"])
    issue.last_refreshed_at = tz_now()
    return issue


def pull_issue(id: str) -> LinearIssue:
    """Fetch an issue by id from the Linear API and save locally."""
    return fetch_issue(id=id).save()
