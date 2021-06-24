import logging

from anymail.inbound import AnymailInboundMessage
from anymail.signals import AnymailInboundEvent, inbound
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpResponse
from django.template import loader

from ..mutations import create_issue

logger = logging.getLogger(__name__)


@receiver(inbound)
def inbound_email(
    sender: object,
    event: AnymailInboundEvent,
    esp_name: str,
    **kwargs: object,
) -> HttpResponse:
    """Receive inbound email and create new issue."""
    message = event.message
    logger.info("Received inbound email from '%s'", message.from_email)
    logger.debug(".. message text:\n%s", message.text)
    logger.debug(".. message html:\n%s", message.html)
    try:
        create_issue(
            team_id=settings.LINEAR_FEEDBACK_TEAM_ID,
            title=message.subject,
            description=_render_description(message),
            label_id=settings.LINEAR_FEEDBACK_LABEL_ID,
        )
    except Exception as ex:
        logger.exception("Error processing inbound email.")
        return HttpResponse(ex)
    else:
        return HttpResponse("OK")


def _render_description(message: AnymailInboundMessage) -> str:
    """Render the issue description from the inbound message."""
    template = loader.get_template("feedback_issue_template.md")
    return template.render(
        {
            "email_from": message.from_email,
            "email_subject": message.subject,
            "email_text": message.text,
        }
    )
