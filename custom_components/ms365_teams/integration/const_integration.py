"""Teams constants."""

from enum import StrEnum

from homeassistant.const import Platform

PLATFORMS: list[Platform] = [Platform.SENSOR]
DOMAIN = "ms365_teams"

ATTR_ACTIVITY = "activity"
ATTR_AVAILABILITY = "availability"
ATTR_CHAT_ID = "chat_id"
ATTR_CHAT_TYPE = "chat_type"
ATTR_CONTENT = "content"
ATTR_CONTENT_TYPE = "content_type"
ATTR_EXPIRATIONDURATION = "expiration_duration"
ATTR_FROM_DISPLAY_NAME = "from_display_name"
ATTR_IMPORTANCE = "importance"
ATTR_MEMBERS = "members"
ATTR_STATUS = "status"
ATTR_SUBJECT = "subject"
ATTR_SUMMARY = "summary"
ATTR_TOPIC = "topic"

CONF_ALTERNATE_EMAIL = "alternate_email"
CONF_CHAT_ENABLE = "chat_enable"
CONF_EMAIL_ACCOUNT = "email_account"
CONF_STATUS_ENABLE = "status_enable"

CONTENT_TYPES = ["text", "html"]

ENTITY_ID_FORMAT_SENSOR = "sensor.{}"

EVENT_SEND_CHAT_MESSAGE = "send_chat_message"
EVENT_UPDATE_USER_STATUS = "update_user_status"
EVENT_UPDATE_USER_PREFERRED_STATUS = "update_user_preferred_status"


PERM_CHAT_READ = "Chat.Read"
PERM_CHAT_READWRITE = "Chat.ReadWrite"
PERM_PRESENCE_READ = "Presence.Read"
PERM_PRESENCE_READ_ALL = "Presence.Read.All"
PERM_PRESENCE_READWRITE = "Presence.ReadWrite"
PERM_USER_READBASIC_ALL = "User.ReadBasic.All"

SENSOR_TEAMS_STATUS = "teams_status"
SENSOR_TEAMS_CHAT = "teams_chat"


class EnableOptions(StrEnum):
    """Teams sensors enablement."""

    DISABLED = "Disabled"
    READ = "Read"
    UPDATE = "Update"
