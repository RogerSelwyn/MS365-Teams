# pylint: disable=unused-argument,line-too-long,wrong-import-order
"""Test main sensors testing."""

from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from requests_mock import Mocker

from ..helpers.mock_config_entry import MS365MockConfigEntry
from ..helpers.utils import check_entity_state, mock_call  # , utcnow
from .const_integration import URL
from .data_integration.state import UPDATE_CHATS
from .helpers_integration.mocks import MS365MOCKS


async def test_get_data(
    hass: HomeAssistant,
    setup_base_integration,
    base_config_entry: MS365MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test get data."""
    entities = er.async_entries_for_config_entry(
        entity_registry, base_config_entry.entry_id
    )
    assert len(entities) == 2

    check_entity_state(
        hass,
        "sensor.test_chat",
        "2020-01-02 00:00:00+00:00",
        attributes={
            "data": None,
            "content": "Test message 1",
            "subject": "Test subject",
            "summary": "Test summary",
        },
    )
    check_entity_state(hass, "sensor.test_status", "Available")


@pytest.mark.parametrize(
    "base_config_entry",
    [{"chat_enable": "Update", "status_enable": "Disabled"}],
    indirect=True,
)
@pytest.mark.parametrize("base_token", ["Chat.ReadWrite"], indirect=True)
async def test_get_update_chat(
    hass: HomeAssistant,
    setup_base_integration,
    base_config_entry: MS365MockConfigEntry,
) -> None:
    """Test get data."""

    check_entity_state(
        hass,
        "sensor.test_chat",
        "2020-01-02 00:00:00+00:00",
        UPDATE_CHATS,
        attributes={"content": "Test message 1"},
    )
    coordinator = base_config_entry.runtime_data.coordinator
    with patch("O365.teams.Chat.get_members") as mock_get_members:
        await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert mock_get_members.call_count == 1


@pytest.mark.parametrize(
    "base_config_entry",
    [{"status_enable": "Disabled"}],
    indirect=True,
)
@pytest.mark.parametrize("base_token", ["Chat.ReadWrite"], indirect=True)
async def test_get_update_chat_systemevent(
    hass: HomeAssistant,
    requests_mock: Mocker,
    base_token,
    base_config_entry: MS365MockConfigEntry,
) -> None:
    """Test get data."""
    MS365MOCKS.standard_mocks(requests_mock)
    mock_call(requests_mock, URL.CHAT1_MESSAGES, "chat1_messages_systemevent")
    base_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(base_config_entry.entry_id)
    await hass.async_block_till_done()

    check_entity_state(
        hass,
        "sensor.test_chat",
        "2020-01-02 00:00:00+00:00",
        attributes={"content": "Test message 3"},
    )


@pytest.mark.parametrize(
    "base_config_entry",
    [{"chat_enable": "Disabled", "alternate_email": "jane@nomail.com"}],
    indirect=True,
)
@pytest.mark.parametrize(
    "base_token", ["Presence.Read Presence.Read.All"], indirect=True
)
async def test_get_other_user_status(
    hass: HomeAssistant,
    setup_base_integration,
    base_config_entry: MS365MockConfigEntry,
) -> None:
    """Test get data."""

    check_entity_state(hass, "sensor.test_status", "Offline")


async def test_run_update(
    hass: HomeAssistant,
    setup_base_integration,
    base_config_entry: MS365MockConfigEntry,
) -> None:
    """Test running coordinator update."""
    coordinator = base_config_entry.runtime_data.coordinator
    with patch(
        "homeassistant.helpers.entity.Entity.async_write_ha_state"
    ) as mock_async_write_ha_state:
        await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert mock_async_write_ha_state.called
