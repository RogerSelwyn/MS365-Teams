"""Sensor processing."""

import logging

from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_ENTITY_KEY, CONF_ENTITY_TYPE
from .helpers.config_entry import MS365ConfigEntry
from .integration.const_integration import (
    CONF_ALTERNATE_EMAIL,
    CONF_CHAT_ENABLE,
    CONF_STATUS_ENABLE,
    PERM_CHAT_READWRITE,
    PERM_PRESENCE_READWRITE,
    SENSOR_TEAMS_CHAT,
    SENSOR_TEAMS_STATUS,
    EnableOptions,
)
from .integration.schema_integration import (
    CHAT_SERVICE_SEND_MESSAGE_SCHEMA,
    STATUS_SERVICE_UPDATE_USER_PERERRED_STATUS_SCHEMA,
    STATUS_SERVICE_UPDATE_USER_STATUS_SCHEMA,
)
from .integration.teamssensor import MS365TeamsChatSensor, MS365TeamsStatusSensor

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    entry: MS365ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MS365 platform."""

    account = entry.runtime_data.account

    is_authenticated = account.is_authenticated
    if not is_authenticated:
        return False

    chat_entities = _chat_entities(entry)
    status_entities = _status_entities(entry)
    entities = chat_entities + status_entities

    async_add_entities(entities, False)
    await _async_setup_register_services(entry)

    return True


def _chat_entities(entry):
    return [
        MS365TeamsChatSensor(
            entry.runtime_data.coordinator,
            entry,
            key[CONF_NAME],
            key[CONF_ENTITY_KEY],
            key[CONF_UNIQUE_ID],
        )
        for key in entry.runtime_data.sensors
        if key[CONF_ENTITY_TYPE] == SENSOR_TEAMS_CHAT
    ]


def _status_entities(entry):
    return [
        MS365TeamsStatusSensor(
            entry.runtime_data.coordinator,
            entry,
            key[CONF_NAME],
            key[CONF_ENTITY_KEY],
            key[CONF_UNIQUE_ID],
            entry.data.get(CONF_ALTERNATE_EMAIL),
        )
        for key in entry.runtime_data.sensors
        if key[CONF_ENTITY_TYPE] == SENSOR_TEAMS_STATUS
    ]


async def _async_setup_register_services(entry):
    perms = entry.runtime_data.permissions
    await _async_setup_status_services(entry, perms)
    await _async_setup_chat_services(entry, perms)


async def _async_setup_status_services(entry, perms):
    if not entry.data[CONF_STATUS_ENABLE] == EnableOptions.UPDATE:
        return

    platform = entity_platform.async_get_current_platform()
    if perms.validate_authorization(PERM_PRESENCE_READWRITE):
        platform.async_register_entity_service(
            "update_user_status",
            STATUS_SERVICE_UPDATE_USER_STATUS_SCHEMA,
            "update_user_status",
        )
        platform.async_register_entity_service(
            "update_user_preferred_status",
            STATUS_SERVICE_UPDATE_USER_PERERRED_STATUS_SCHEMA,
            "update_user_preferred_status",
        )


async def _async_setup_chat_services(entry, perms):
    if not entry.data[CONF_CHAT_ENABLE] == EnableOptions.UPDATE:
        return

    platform = entity_platform.async_get_current_platform()
    if perms.validate_authorization(PERM_CHAT_READWRITE):
        platform.async_register_entity_service(
            "send_chat_message",
            CHAT_SERVICE_SEND_MESSAGE_SCHEMA,
            "send_chat_message",
        )
