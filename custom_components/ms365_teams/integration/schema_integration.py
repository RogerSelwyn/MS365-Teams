"""Schema for MS365 Integration."""

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.notify import ATTR_MESSAGE
from O365.teams import (  # pylint: disable=import-error, no-name-in-module
    Activity,
    Availability,
    PreferredAvailability,
)

from .const_integration import (
    ATTR_ACTIVITY,
    ATTR_AVAILABILITY,
    ATTR_CHAT_ID,
    ATTR_CONTENT_TYPE,
    ATTR_EXPIRATIONDURATION,
    CONF_ALTERNATE_EMAIL,
    CONF_CHAT_ENABLE,
    CONF_STATUS_ENABLE,
    CONTENT_TYPES,
    EnableOptions,
)

CONFIG_SCHEMA_INTEGRATION = {
    vol.Required(CONF_CHAT_ENABLE, default=EnableOptions.READ): vol.In(EnableOptions),
    vol.Required(CONF_STATUS_ENABLE, default=EnableOptions.READ): vol.In(EnableOptions),
    vol.Optional(CONF_ALTERNATE_EMAIL): cv.string,
}

CHAT_SERVICE_SEND_MESSAGE_SCHEMA = {
    vol.Required(ATTR_CHAT_ID): cv.string,
    vol.Required(ATTR_MESSAGE): cv.string,
    vol.Optional(ATTR_CONTENT_TYPE, default="text"): vol.In(CONTENT_TYPES),
}

STATUS_SERVICE_UPDATE_USER_STATUS_SCHEMA = {
    vol.Required(ATTR_AVAILABILITY): vol.Coerce(Availability),
    vol.Required(ATTR_ACTIVITY): vol.Coerce(Activity),
    vol.Optional(ATTR_EXPIRATIONDURATION): cv.string,
}

STATUS_SERVICE_UPDATE_USER_PERERRED_STATUS_SCHEMA = {
    vol.Required(ATTR_AVAILABILITY): vol.Coerce(PreferredAvailability),
    vol.Optional(ATTR_EXPIRATIONDURATION): cv.string,
}
