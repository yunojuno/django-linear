import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now as tz_now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import LinearIssue

logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_staff)
def import_issues(request: HttpRequest) -> HttpResponseRedirect:
    if not request.user.has_perms("linear.use_api"):
        messages.add_message(
            request, messages.ERROR, "You do not permission to use the Linear API"
        )
    else:
        call_command("import_issues")
        messages.add_message(
            request,
            messages.SUCCESS,
            "All Linear issues have been imported successfully",
        )
    return HttpResponseRedirect(reverse("admin:linear_linearissue_changelist"))


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
        body = json.loads(request.body.decode("utf-8"))
        data = body["data"]
        if body["type"] != "Issue":
            return HttpResponse("We are not interested in non-Issue updates")
    except (json.JSONDecodeError, KeyError):
        logger.exception("Unable to process Linear webhook event")
        return HttpResponse(
            "We couldn't process the request, but we're sending back a 200 anyway."
        )

    # we always get id, team, state in the payload. project/milestone are not included.
    id = data["id"]
    title = data["title"]
    team_name = data["team"]["name"]
    state = data["state"]["name"]
    estimate = data.get("estimate")
    identifier = f'{data["team"]["key"]}-{data["number"]}'

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
