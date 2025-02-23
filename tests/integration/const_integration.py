# pylint: disable=unused-import
"""Constants for mail integration."""

from copy import deepcopy
from enum import Enum

from custom_components.ms365_teams.config_flow import MS365ConfigFlow  # noqa: F401
from custom_components.ms365_teams.const import (  # noqa: F401
    AUTH_CALLBACK_PATH_ALT,
    COUNTRY_URLS,
    OAUTH_REDIRECT_URL,
    CountryOptions,
)
from custom_components.ms365_teams.integration.const_integration import (
    DOMAIN,  # noqa: F401
)

from ..const import CLIENT_ID, CLIENT_SECRET, ENTITY_NAME

AUTH_CALLBACK_PATH_DEFAULT = COUNTRY_URLS[CountryOptions.DEFAULT][OAUTH_REDIRECT_URL]
BASE_CONFIG_ENTRY = {
    "entity_name": ENTITY_NAME,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "alt_auth_method": False,
    "chat_enable": "Read",
    "status_enable": "Read",
    "api_options": {"country": "Default"},
}
BASE_TOKEN_PERMS = "Chat.Read Presence.Read"
BASE_MISSING_PERMS = "Chat.Read, Presence.Read"
UPDATE_TOKEN_PERMS = "Chat.ReadWrite Presence.ReadWrite"
UPDATE_OPTIONS = {"chat_enable": "Update", "status_enable": "Update"}

ALT_CONFIG_ENTRY = deepcopy(BASE_CONFIG_ENTRY)
ALT_CONFIG_ENTRY["alt_auth_method"] = True
COUNTRY_CONFIG_ENTRY = deepcopy(BASE_CONFIG_ENTRY)
COUNTRY_CONFIG_ENTRY["api_options"]["country"] = "21Vianet (China)"

RECONFIGURE_CONFIG_ENTRY = deepcopy(BASE_CONFIG_ENTRY)
del RECONFIGURE_CONFIG_ENTRY["entity_name"]

MIGRATION_CONFIG_ENTRY = {
    "data": BASE_CONFIG_ENTRY,
    "options": {},
}

DIAGNOSTIC_GRANTED_PERMISSIONS = [
    "Chat.Read",
    "Presence.Read",
    "User.Read",
    "email",
    "openid",
    "profile",
]
DIAGNOSTIC_REQUESTED_PERMISSIONS = [
    "User.Read",
    "Chat.Read",
    "Presence.Read",
]

FULL_INIT_ENTITY_NO = 2


class URL(Enum):
    """List of URLs"""

    OPENID = (
        "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    )
    ME = "https://graph.microsoft.com/v1.0/me"
    CHATS = "https://graph.microsoft.com/v1.0/me/chats"
    CHAT1_MESSAGES = "https://graph.microsoft.com/v1.0//chats/chat1/messages"
    CHAT1_MEMBERS = "https://graph.microsoft.com/v1.0//chats/chat1/members"
    CHAT2_MESSAGES = "https://graph.microsoft.com/v1.0//chats/chat2/messages"
    CHAT2_MEMBERS = "https://graph.microsoft.com/v1.0//chats/chat2/members"
    PRESENCE = "https://graph.microsoft.com/v1.0/me/presence"
    ALTERNATE_PRESENCE = "https://graph.microsoft.com/v1.0/users/fake_user_id2/presence"
    ALTERNATE_USER = "https://graph.microsoft.com/v1.0/users/jane@nomail.com"


class CN21VURL(Enum):
    """List of URLs"""

    DISCOVERY = "https://login.microsoftonline.com/common/discovery/instance"
    OPENID = "https://login.partner.microsoftonline.cn/common/v2.0/.well-known/openid-configuration"
    ME = "https://microsoftgraph.chinacloudapi.cn/v1.0/me"
    CHATS = "https://microsoftgraph.chinacloudapi.cn/v1.0/me/chats"
    CHAT1_MESSAGES = (
        "https://microsoftgraph.chinacloudapi.cn/v1.0//chats/chat1/messages"
    )
    PRESENCE = "https://microsoftgraph.chinacloudapi.cn/v1.0/me/presence"
