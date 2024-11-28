"""MS365 teams sensors."""

import functools as ft
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_NAME, CONF_EMAIL, CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from O365.teams import (  # pylint: disable=import-error, no-name-in-module
    PreferredActivity,
    PreferredAvailability,
)

from ..classes.entity import MS365Entity
from ..const import (
    ATTR_DATA,
    ATTR_STATE,
    CONF_CLIENT_ID,
    CONF_ENTITY_KEY,
    CONF_ENTITY_TYPE,
    EVENT_HA_EVENT,
)
from ..helpers.config_entry import MS365ConfigEntry
from .const_integration import (
    ATTR_ACTIVITY,
    ATTR_AVAILABILITY,
    ATTR_CHAT_ID,
    ATTR_CONTENT,
    ATTR_FROM_DISPLAY_NAME,
    ATTR_IMPORTANCE,
    ATTR_STATUS,
    ATTR_SUBJECT,
    ATTR_SUMMARY,
    CONF_ALTERNATE_EMAIL,
    CONF_CHAT_ENABLE,
    CONF_STATUS_ENABLE,
    DOMAIN,
    EVENT_SEND_CHAT_MESSAGE,
    EVENT_UPDATE_USER_PREFERRED_STATUS,
    EVENT_UPDATE_USER_STATUS,
    PERM_CHAT_READWRITE,
    PERM_PRESENCE_READWRITE,
    SENSOR_TEAMS_CHAT,
    SENSOR_TEAMS_STATUS,
    EnableOptions,
)
from .schema_integration import (
    CHAT_SERVICE_SEND_MESSAGE_SCHEMA,
    STATUS_SERVICE_UPDATE_USER_PERERRED_STATUS_SCHEMA,
    STATUS_SERVICE_UPDATE_USER_STATUS_SCHEMA,
)

_LOGGER = logging.getLogger(__name__)


async def async_integration_setup_entry(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    entry: MS365ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MS365 platform."""

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
    if entry.data[CONF_STATUS_ENABLE] != EnableOptions.UPDATE:
        return

    platform = entity_platform.async_get_current_platform()
    if perms.validate_authorization(PERM_PRESENCE_READWRITE):
        platform.async_register_entity_service(
            "update_user_status",
            STATUS_SERVICE_UPDATE_USER_STATUS_SCHEMA,
            "async_update_user_status",
        )
        platform.async_register_entity_service(
            "update_user_preferred_status",
            STATUS_SERVICE_UPDATE_USER_PERERRED_STATUS_SCHEMA,
            "async_update_user_preferred_status",
        )


async def _async_setup_chat_services(entry, perms):
    if entry.data[CONF_CHAT_ENABLE] != EnableOptions.UPDATE:
        return

    platform = entity_platform.async_get_current_platform()
    if perms.validate_authorization(PERM_CHAT_READWRITE):
        platform.async_register_entity_service(
            "send_chat_message",
            CHAT_SERVICE_SEND_MESSAGE_SCHEMA,
            "async_send_chat_message",
        )


class MS365TeamsSensor(MS365Entity):
    """MS365 Teams sensor processing."""

    _attr_translation_key = "teams"

    def __init__(
        self, coordinator, entry: MS365ConfigEntry, name, entity_id, unique_id
    ):
        """Initialise the Teams Sensor."""
        super().__init__(coordinator, entry, name, entity_id, unique_id)
        self.teams = self._entry.runtime_data.account.teams()
        self._application_id = entry.data[CONF_CLIENT_ID]

    @property
    def native_value(self):
        """Sensor state."""
        return self.coordinator.data[self.entity_key][ATTR_STATE]


class MS365TeamsStatusSensor(MS365TeamsSensor, SensorEntity):
    """O365 Teams sensor processing."""

    def __init__(
        self,
        coordinator,
        entry: MS365ConfigEntry,
        name,
        entity_id,
        unique_id,
        email,
    ):
        """Initialise the Teams Sensor."""
        super().__init__(coordinator, entry, name, entity_id, unique_id)
        self._email = email

    async def async_update_user_status(
        self, availability, activity, expiration_duration=None
    ):
        """Update the users teams status."""
        if self._email:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="not_possible",
                translation_placeholders={
                    CONF_EMAIL: self._email,
                },
            )

        self._validate_status_permissions()

        status = await self.hass.async_add_executor_job(
            self.teams.set_my_presence,
            self._application_id,
            availability,
            activity,
            expiration_duration,
        )
        self._raise_event(
            EVENT_UPDATE_USER_STATUS,
            {ATTR_AVAILABILITY: status.availability, ATTR_ACTIVITY: status.activity},
        )
        return False

    async def async_update_user_preferred_status(
        self, availability, expiration_duration=None
    ):
        """Update the users teams status."""
        if self._email:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="not_possible",
                translation_placeholders={
                    CONF_EMAIL: self._email,
                },
            )

        self._validate_status_permissions()

        activity = (
            availability
            if availability != PreferredAvailability.OFFLINE
            else PreferredActivity.OFFWORK
        )
        status = await self.hass.async_add_executor_job(
            self.teams.set_my_user_preferred_presence,
            availability,
            activity,
            expiration_duration,
        )
        self._raise_event(
            EVENT_UPDATE_USER_PREFERRED_STATUS,
            {ATTR_AVAILABILITY: status.availability, ATTR_ACTIVITY: status.activity},
        )
        return False

    def _raise_event(self, event_type, status):
        self.hass.bus.fire(
            f"{DOMAIN}_{event_type}",
            {ATTR_NAME: self._name, ATTR_STATUS: status, EVENT_HA_EVENT: True},
        )
        _LOGGER.debug("%s - %s - %s", self._name, event_type, status)

    def _validate_status_permissions(self):
        return self._validate_permissions(
            PERM_PRESENCE_READWRITE,
            f"Not authorised to update status - requires permission: {PERM_PRESENCE_READWRITE}",
        )


class MS365TeamsChatSensor(MS365TeamsSensor, SensorEntity):
    """O365 Teams Chat sensor processing."""

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        attributes = {
            ATTR_FROM_DISPLAY_NAME: self.coordinator.data[self.entity_key][
                ATTR_FROM_DISPLAY_NAME
            ],
            ATTR_CONTENT: self.coordinator.data[self.entity_key][ATTR_CONTENT],
            ATTR_CHAT_ID: self.coordinator.data[self.entity_key][ATTR_CHAT_ID],
            ATTR_IMPORTANCE: self.coordinator.data[self.entity_key][ATTR_IMPORTANCE],
        }
        if self.coordinator.data[self.entity_key][ATTR_SUBJECT]:
            attributes[ATTR_SUBJECT] = self.coordinator.data[self.entity_key][
                ATTR_SUBJECT
            ]
        if self.coordinator.data[self.entity_key][ATTR_SUMMARY]:
            attributes[ATTR_SUMMARY] = self.coordinator.data[self.entity_key][
                ATTR_SUMMARY
            ]
        if self.coordinator.data[self.entity_key][ATTR_DATA]:
            attributes[ATTR_DATA] = self.coordinator.data[self.entity_key][ATTR_DATA]
        return attributes

    async def async_send_chat_message(self, chat_id, message, content_type):
        """Send a message to the specified chat."""
        self._validate_chat_permissions()

        chats = await self.hass.async_add_executor_job(self.teams.get_my_chats)
        for chat in chats:
            if chat.object_id == chat_id:
                message = await self.hass.async_add_executor_job(
                    ft.partial(
                        chat.send_message, content=message, content_type=content_type
                    )
                )
                self._raise_event(EVENT_SEND_CHAT_MESSAGE, chat_id)
                return True
        _LOGGER.warning("Chat %s not found for send message", chat_id)
        return False

    def _raise_event(self, event_type, chat_id):
        self.hass.bus.fire(
            f"{DOMAIN}_{event_type}",
            {ATTR_CHAT_ID: chat_id, EVENT_HA_EVENT: True},
        )
        _LOGGER.debug("%s - %s", event_type, chat_id)

    def _validate_chat_permissions(self):
        return self._validate_permissions(
            PERM_CHAT_READWRITE,
            f"Not authorised to send message - requires permission: {PERM_CHAT_READWRITE}",
        )
