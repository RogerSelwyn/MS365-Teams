# pylint: disable=line-too-long, unused-argument
"""Test the config flow."""

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from requests_mock import Mocker

from ..const import CLIENT_ID, CLIENT_SECRET, ENTITY_NAME
from ..helpers.mock_config_entry import MS365MockConfigEntry
from ..helpers.utils import mock_token
from .const_integration import BASE_TOKEN_PERMS, DOMAIN
from .helpers_integration.mocks import MS365MOCKS


async def test_invalid_config(
    hass: HomeAssistant,
    requests_mock: Mocker,
) -> None:
    """Test the default config_flow."""
    mock_token(requests_mock, BASE_TOKEN_PERMS)
    MS365MOCKS.standard_mocks(requests_mock)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "entity_name": ENTITY_NAME,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "alt_auth_method": False,
            "chat_enable": "Disabled",
            "status_enable": "Update",
            "alternate_email": "jane@nomail.com",
        },
    )
    print(result)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert "errors" in result
    assert "status_enable" in result["errors"]
    assert result["errors"]["status_enable"] == "status_enable_should_be_read"


async def test_options_flow(
    hass: HomeAssistant,
    setup_base_integration,
    base_config_entry: MS365MockConfigEntry,
) -> None:
    """Test the options flow"""

    result = await hass.config_entries.options.async_init(base_config_entry.entry_id)
    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert "result" in result
    assert result["result"] is True
    assert result["data"] is None
