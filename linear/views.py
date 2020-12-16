import json
import logging
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now as tz_now

from .models import LinearIssue

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request: HttpRequest) -> HttpResponse:
    """
    Process Linear webhook event.

    This webhook currently only listens for Issue events, and it treats both
    "Create" and "Update" events in the same way. It will set the identifier,
    team_name, title, state and estimate fields. The project_name and
    milestone_name are not included in the webhook payload.

    """
    try:
        body = json.loads(request.body.decode('utf-8'))
        data = body["data"]
        _type = body["type"]
        if _type != "Issue":
            return HttpResponse("We are not interested in non-Issue updates")
    except:
        logger.exception("Unable to process Linear webhook event")
        return HttpResponse("We couldn't process the request, but we're sending back a 200 anyway.")

    # we always get id, team, state in the payload. project/milestone are not included.
    id=data["id"]
    title=data["title"]
    team_name=data["team"]["name"]
    state=data["state"]["name"]
    estimate=data.get("estimate")
    identifier=f'{data["team"]["key"]}-{data["number"]}'

    try:
        issue = LinearIssue.objects.get(id=id)
    except LinearIssue.DoesNotExist:
        issue = LinearIssue.objects.create(id=id)

    issue.title = title
    issue.state = state
    issue.estimate = estimate
    issue.team_name = team_name
    issue.identifier = identifier
    issue.last_refreshed_at = tz_now()
    issue.save()
    return HttpResponse("Task updated")
