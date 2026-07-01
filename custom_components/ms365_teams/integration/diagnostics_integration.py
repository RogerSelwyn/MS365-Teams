"""Diagnostics support for MS365."""

from homeassistant.core import HomeAssistant

from ..classes.config_entry import MS365ConfigEntry


async def async_integration_diagnostics(hass: HomeAssistant, entry: MS365ConfigEntry):  # pylint: disable=unused-argument
    """Get integration specific diagnostics."""

    return None
