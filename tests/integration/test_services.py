# pylint: disable=unused-argument,line-too-long,wrong-import-order
"""Test service usage."""

from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError

from custom_components.ms365_teams.integration.const_integration import (
    CONF_CHAT_ENABLE,
    CONF_STATUS_ENABLE,
)

from ..conftest import MS365MockConfigEntry
from .const_integration import DOMAIN


async def test_update_service_setup(
    hass: HomeAssistant,
    setup_update_integration,
    base_config_entry: MS365MockConfigEntry,
) -> None:
    """Test the reconfigure flow."""
    assert base_config_entry.data[CONF_CHAT_ENABLE] == "Update"
    assert base_config_entry.data[CONF_STATUS_ENABLE] == "Update"
    assert hass.services.has_service(DOMAIN, "update_user_status")
    assert hass.services.has_service(DOMAIN, "update_user_preferred_status")
    assert hass.services.has_service(DOMAIN, "send_chat_message")


@pytest.mark.parametrize(
    "base_config_entry",
    [{"chat_enable": "Update", "status_enable": "Disabled"}],
    indirect=True,
)
@pytest.mark.parametrize("base_token", ["Chat.ReadWrite"], indirect=True)
async def test_chat_services(
    hass: HomeAssistant,
    setup_base_integration,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test chat services"""
    entity_name = "sensor.test_chat"
    with patch("O365.teams.Chat.send_message") as mock_send_message:
        await hass.services.async_call(
            DOMAIN,
            "send_chat_message",
            {
                "entity_id": entity_name,
                "chat_id": "chat1",
                "message": "Test message",
                "content_type": "text",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert mock_send_message.called

    await hass.services.async_call(
        DOMAIN,
        "send_chat_message",
        {
            "entity_id": entity_name,
            "chat_id": "chat99",
            "message": "Test message",
            "content_type": "text",
        },
        blocking=True,
        return_response=False,
    )
    await hass.async_block_till_done()
    assert "Chat chat99 not found for send message" in caplog.text


@pytest.mark.parametrize(
    "base_config_entry",
    [{"status_enable": "Update", "chat_enable": "Disabled"}],
    indirect=True,
)
@pytest.mark.parametrize("base_token", ["Presence.ReadWrite"], indirect=True)
async def test_presence_services(
    hass: HomeAssistant,
    setup_base_integration,
) -> None:
    """Test presence services"""
    entity_name = "sensor.test_status"
    with patch("O365.teams.Teams.set_my_presence") as mock_set_presence:
        await hass.services.async_call(
            DOMAIN,
            "update_user_status",
            {
                "entity_id": entity_name,
                "availability": "Busy",
                "activity": "InACall",
                "expiration_duration": "PT1H",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert mock_set_presence.called

    with patch("O365.teams.Teams.set_my_user_preferred_presence") as mock_set_presence:
        await hass.services.async_call(
            DOMAIN,
            "update_user_preferred_status",
            {
                "entity_id": entity_name,
                "availability": "Busy",
                "expiration_duration": "PT1H",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert mock_set_presence.called


@pytest.mark.parametrize(
    "base_config_entry",
    [
        {
            "status_enable": "Update",
            "chat_enable": "Disabled",
            "alternate_email": "jane@nomail.com",
        }
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "base_token", ["Presence.ReadWrite Presence.Read.All"], indirect=True
)
async def test_presence_service_failures(
    hass: HomeAssistant,
    setup_base_integration,
) -> None:
    """Testchat services"""
    entity_name = "sensor.test_status"
    with pytest.raises(ServiceValidationError) as exc_info:
        await hass.services.async_call(
            DOMAIN,
            "update_user_status",
            {
                "entity_id": entity_name,
                "availability": "Busy",
                "activity": "InACall",
                "expiration_duration": "PT1H",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert "Not possible to update alternate user status: jane@nomail.com" in str(
        exc_info.value
    )

    with pytest.raises(ServiceValidationError) as exc_info:
        await hass.services.async_call(
            DOMAIN,
            "update_user_preferred_status",
            {
                "entity_id": entity_name,
                "availability": "Busy",
                "expiration_duration": "PT1H",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert "Not possible to update alternate user status: jane@nomail.com" in str(
        exc_info.value
    )


@pytest.mark.parametrize(
    "base_config_entry",
    [{"chat_enable": "Update", "status_enable": "Disabled"}],
    indirect=True,
)
@pytest.mark.parametrize("base_token", ["Chat.ReadWrite"], indirect=True)
async def test_chat_failed_permission(
    hass: HomeAssistant,
    setup_base_integration,
) -> None:
    """Test notify - HA Service."""
    entity_name = "sensor.test_chat"
    failed_perm = "teams.failed_perm"
    with (
        patch(
            f"custom_components.{DOMAIN}.integration.sensor_integration.PERM_CHAT_READWRITE",
            failed_perm,
        ),
        pytest.raises(ServiceValidationError) as exc_info,
    ):
        await hass.services.async_call(
            DOMAIN,
            "send_chat_message",
            {
                "entity_id": entity_name,
                "chat_id": "chat1",
                "message": "Test message",
                "content_type": "text",
            },
            blocking=True,
            return_response=False,
        )
    assert (
        f"Not authorised to send message - requires permission: {failed_perm}"
        in str(exc_info.value)
    )


@pytest.mark.parametrize(
    "base_config_entry",
    [{"status_enable": "Update", "chat_enable": "Disabled"}],
    indirect=True,
)
@pytest.mark.parametrize("base_token", ["Presence.ReadWrite"], indirect=True)
async def test_presence_failed_permission(
    hass: HomeAssistant,
    setup_base_integration,
) -> None:
    """Testchat services"""
    entity_name = "sensor.test_status"
    failed_perm = "teams.failed_perm"
    with (
        patch(
            f"custom_components.{DOMAIN}.integration.sensor_integration.PERM_PRESENCE_READWRITE",
            failed_perm,
        ),
        pytest.raises(ServiceValidationError) as exc_info,
    ):
        await hass.services.async_call(
            DOMAIN,
            "update_user_status",
            {
                "entity_id": entity_name,
                "availability": "Busy",
                "activity": "InACall",
                "expiration_duration": "PT1H",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert (
        f"Not authorised to update status - requires permission: {failed_perm}"
        in str(exc_info.value)
    )

    with (
        patch(
            f"custom_components.{DOMAIN}.integration.sensor_integration.PERM_PRESENCE_READWRITE",
            failed_perm,
        ),
        pytest.raises(ServiceValidationError) as exc_info,
    ):
        await hass.services.async_call(
            DOMAIN,
            "update_user_preferred_status",
            {
                "entity_id": entity_name,
                "availability": "Busy",
                "expiration_duration": "PT1H",
            },
            blocking=True,
            return_response=False,
        )
    await hass.async_block_till_done()
    assert (
        f"Not authorised to update status - requires permission: {failed_perm}"
        in str(exc_info.value)
    )
