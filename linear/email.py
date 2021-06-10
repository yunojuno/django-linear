"""Central module which checks and routes inbound email handling."""
from __future__ import annotations

import logging
from typing import Any

from anymail.signals import AnymailInboundEvent, inbound
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpResponse

from linear.mutations import create_issue

logger = logging.getLogger(__name__)


@receiver(inbound)
def inbound_email_wrapper(
    sender: object,
    event: AnymailInboundEvent,
    esp_name: str,
    **kwargs: Any,
) -> HttpResponse:
    """Receive anymail inbound email signal and pass on to existing function."""
    logger.info("Received inbound email from '%s'", event.message.from_email)
    logger.debug(".. message text:\n%s", event.message.text)
    logger.debug(".. message html:\n%s", event.message.html)
    try:
        return create_issue(
            team_id=settings.LINEAR_FEEDBACK_TEAM_ID,
            title=event.message.subject,
            description=event.message.text,
            label_id=settings.LINEAR_FEEDBACK_LABEL_ID,
        )
    except Exception:
        logger.exception("Error processing inbound email.")
    return HttpResponse("OK")
