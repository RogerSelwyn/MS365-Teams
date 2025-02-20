"""Configuration flow for the MS365 platform."""

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import (
    config_entries,
)
from homeassistant.data_entry_flow import FlowResult

from ..classes.config_entry import MS365ConfigEntry
from ..const import CONF_ENTITY_NAME
from .const_integration import (
    CONF_ALTERNATE_EMAIL,
    CONF_CHAT_ENABLE,
    CONF_STATUS_ENABLE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    EnableOptions,
)


def integration_reconfigure_schema(entry_data):
    """Extend the schema with integration specific attributes."""
    return {
        vol.Required(CONF_CHAT_ENABLE, default=entry_data[CONF_CHAT_ENABLE]): vol.In(
            EnableOptions
        ),
        vol.Required(
            CONF_STATUS_ENABLE, default=entry_data[CONF_STATUS_ENABLE]
        ): vol.In(EnableOptions),
        vol.Optional(
            CONF_ALTERNATE_EMAIL,
            description={"suggested_value": entry_data.get(CONF_ALTERNATE_EMAIL)},
        ): cv.string,
    }


def integration_validate_schema(user_input):
    """Validate the user input."""
    if (
        user_input.get(CONF_ALTERNATE_EMAIL)
        and user_input.get(CONF_STATUS_ENABLE) != EnableOptions.READ
    ):
        return {CONF_STATUS_ENABLE: "status_enable_should_be_read"}
    return {}


async def async_integration_imports(hass, import_data):  # pylint: disable=unused-argument
    """Do the integration  level import tasks."""
    return


class MS365OptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options for MS365."""

    def __init__(self, entry: MS365ConfigEntry):
        """Initialize MS365 options flow."""

    async def async_step_init(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Set up the option flow."""

        return await self.async_step_user()

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""

        errors = {}

        if user_input:
            return await self._async_tidy_up(user_input)

        return self.async_show_form(
            step_id="user",
            description_placeholders={
                CONF_ENTITY_NAME: self.config_entry.data[CONF_ENTITY_NAME]
            },
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
                }
            ),
            errors=errors,
            last_step=True,
        )

    async def _async_tidy_up(self, user_input):
        update = self.async_create_entry(title="", data=user_input)
        await self.hass.config_entries.async_reload(self._config_entry_id)
        return update
