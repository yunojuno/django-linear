import uuid
from unittest import mock

import pytest
from anymail.inbound import AnymailInboundMessage
from anymail.signals import AnymailInboundEvent, EventType
from anymail.webhooks.postmark import PostmarkInboundWebhookView
from django.test import override_settings

from linear.signals.handlers import _render_description, inbound_email


@pytest.fixture
def message() -> AnymailInboundMessage:
    message = AnymailInboundMessage.construct(
        from_email="from@example.com",
        to="to@example.com",
        cc="cc@example.com",
        subject="test subject",
        text="Test email",
    )
    assert message.text == "Test email"
    assert message.from_email.address == "from@example.com"
    assert message.subject == "test subject"
    return message


@pytest.fixture
def event(message) -> AnymailInboundEvent:
    return AnymailInboundEvent(
        event_type=EventType.INBOUND,
        timestamp=None,  # Postmark doesn't provide inbound event timestamp
        event_id=uuid.uuid4(),  # Postmark uuid, different from Message-ID mime header
        message=message,
    )


@override_settings(LINEAR_FEEDBACK_TEAM_ID="123", LINEAR_FEEDBACK_LABEL_ID="456")
@mock.patch("linear.signals.handlers.create_issue")
def test_inbound_email(mock_create, event: AnymailInboundEvent) -> None:
    resp = inbound_email(PostmarkInboundWebhookView, event, "postmark")
    assert resp.status_code == 200
    mock_create.assert_called_once_with(
        team_id="123",
        title="test subject",
        description=_render_description(event.message),
        label_id="456",
    )


@mock.patch("linear.signals.handlers.create_issue")
def test_inbound_email__error(mock_create, event: AnymailInboundEvent) -> None:
    # confirm that we still get a 200 even when there is an error.
    mock_create.side_effect = Exception("Unexpected item in the bagging area")
    resp = inbound_email(PostmarkInboundWebhookView, event, "postmark")
    assert resp.status_code == 200
    assert resp.content.decode() == "Unexpected item in the bagging area"


def test__render_description(message: AnymailInboundMessage) -> None:
    assert _render_description(message) == (
        "Test email\n___\nFeedback via email from from@example.com\n"
    )
