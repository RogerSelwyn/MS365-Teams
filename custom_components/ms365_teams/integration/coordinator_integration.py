"""Sensor processing."""

import functools as ft
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..const import (
    ATTR_DATA,
    ATTR_STATE,
    CONF_ENTITY_KEY,
    CONF_ENTITY_NAME,
    CONF_ENTITY_TYPE,
)
from ..helpers.utils import build_entity_id
from .const_integration import (
    ATTR_CHAT_ID,
    ATTR_CHAT_TYPE,
    ATTR_CONTENT,
    ATTR_FROM_DISPLAY_NAME,
    ATTR_IMPORTANCE,
    ATTR_MEMBERS,
    ATTR_SUBJECT,
    ATTR_SUMMARY,
    ATTR_TOPIC,
    CONF_ALTERNATE_EMAIL,
    CONF_CHAT_ENABLE,
    CONF_EMAIL_ACCOUNT,
    CONF_STATUS_ENABLE,
    ENTITY_ID_FORMAT_SENSOR,
    SENSOR_TEAMS_CHAT,
    SENSOR_TEAMS_STATUS,
    EnableOptions,
)

_LOGGER = logging.getLogger(__name__)


class MS365SensorCoordinator(DataUpdateCoordinator):
    """MS365 sensor data update coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, account):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="MS365 Teams",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
        )
        self._entry = entry
        self._account = account
        self._entity_name = entry.data[CONF_ENTITY_NAME]
        self.keys = []
        self._data = {}
        self._chat_members = {}

    async def _async_setup(self):
        """Do the initial setup of the entities."""
        status_keys = await self._async_status_sensors()
        chat_keys = self._chat_sensors()
        self.keys = chat_keys + status_keys
        return self.keys

    async def _async_status_sensors(self):
        keys = []

        if self._entry.data[CONF_STATUS_ENABLE] != EnableOptions.DISABLED:
            name = f"{self._entry.data[CONF_ENTITY_NAME]}_status"
            new_key = {
                CONF_ENTITY_KEY: build_entity_id(
                    self.hass, ENTITY_ID_FORMAT_SENSOR, name
                ),
                CONF_UNIQUE_ID: f"{name}_ms365",
                CONF_NAME: name,
                CONF_ENTITY_TYPE: SENSOR_TEAMS_STATUS,
            }

            if email := self._entry.data.get(CONF_ALTERNATE_EMAIL):
                email_account = await self.hass.async_add_executor_job(
                    self._account.directory().get_user,
                    email,
                )
                new_key[CONF_EMAIL_ACCOUNT] = email_account.object_id

            keys.append(new_key)
        return keys

    def _chat_sensors(self):
        keys = []

        if self._entry.data[CONF_CHAT_ENABLE] != EnableOptions.DISABLED:
            name = f"{self._entry.data[CONF_ENTITY_NAME]}_chat"
            new_key = {
                CONF_ENTITY_KEY: build_entity_id(
                    self.hass, ENTITY_ID_FORMAT_SENSOR, name
                ),
                CONF_UNIQUE_ID: f"{name}_ms365",
                CONF_NAME: name,
                CONF_ENTITY_TYPE: SENSOR_TEAMS_CHAT,
            }

            keys.append(new_key)
        return keys

    async def _async_update_data(self):
        _LOGGER.debug(
            "Doing %s email update(s) for: %s", len(self.keys), self._entity_name
        )

        for key in self.keys:
            entity_type = key[CONF_ENTITY_TYPE]
            if entity_type == SENSOR_TEAMS_CHAT:
                await self._async_teams_chat_update(key)
            elif entity_type == SENSOR_TEAMS_STATUS:
                await self._async_teams_status_update(key)

        return self._data

    async def _async_teams_status_update(self, key):
        """Update state."""
        entity_key = key[CONF_ENTITY_KEY]
        email_account = key.get(CONF_EMAIL_ACCOUNT)
        if not email_account:
            if data := await self.hass.async_add_executor_job(
                self._account.teams().get_my_presence
            ):
                self._data[entity_key] = {ATTR_STATE: data.activity}
            return
        if data := await self.hass.async_add_executor_job(
            self._account.teams().get_user_presence, email_account
        ):
            self._data[entity_key] = {ATTR_STATE: data.activity}

    async def _async_teams_chat_update(self, key):
        entity_key = key[CONF_ENTITY_KEY]
        state = None
        data = []
        self._data[entity_key] = {}
        extra_attributes = {}
        chats = await self.hass.async_add_executor_job(
            ft.partial(self._account.teams().get_my_chats, limit=20)
        )
        for chat in chats:
            if chat.chat_type == "unknownFutureValue":
                continue
            if not state:
                messages = await self.hass.async_add_executor_job(
                    ft.partial(chat.get_messages, limit=10)
                )
                state, extra_attributes = self._process_chat_messages(messages)

            if self._entry.data[CONF_CHAT_ENABLE] == EnableOptions.UPDATE:
                memberlist = await self._async_get_memberlist(chat)
                chatitems = {
                    ATTR_CHAT_ID: chat.object_id,
                    ATTR_CHAT_TYPE: chat.chat_type,
                    ATTR_MEMBERS: ",".join(memberlist),
                }
            elif state:
                break
            else:
                continue
            if chat.chat_type == "group":
                chatitems[ATTR_TOPIC] = chat.topic

            data.append(chatitems)

        self._data[entity_key] = (
            {ATTR_STATE: state} | extra_attributes | {ATTR_DATA: data}
        )

    def _process_chat_messages(self, messages):
        state = None
        extra_attributes = {}
        for message in messages:
            if not state and message.content != "<systemEventMessage/>":
                state = message.created_date
                extra_attributes = {
                    ATTR_FROM_DISPLAY_NAME: message.from_display_name,
                    ATTR_CONTENT: message.content,
                    ATTR_CHAT_ID: message.chat_id,
                    ATTR_IMPORTANCE: message.importance,
                    ATTR_SUBJECT: message.subject,
                    ATTR_SUMMARY: message.summary,
                }
                break
        return state, extra_attributes

    async def _async_get_memberlist(self, chat):
        if chat.object_id in self._chat_members and chat.chat_type != "oneOnOne":
            return self._chat_members[chat.object_id]
        members = await self.hass.async_add_executor_job(chat.get_members)
        memberlist = []
        for member in members:
            if member.display_name:
                memberlist.append(member.display_name)
            elif member.email:
                memberlist.append(member.email)
            else:
                memberlist.append("Name Unknown")
        self._chat_members[chat.object_id] = memberlist
        return memberlist
