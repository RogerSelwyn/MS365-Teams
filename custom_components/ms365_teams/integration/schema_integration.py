"""Schema for MS365 Integration."""

import probatio

from homeassistant.components.notify import ATTR_MESSAGE
import homeassistant.helpers.config_validation as cv
from O365.teams import Activity, Availability, PreferredAvailability  # pylint: disable=import-error, no-name-in-module

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
    probatio.Required(CONF_CHAT_ENABLE, default=EnableOptions.READ): probatio.In(
        EnableOptions
    ),
    probatio.Required(CONF_STATUS_ENABLE, default=EnableOptions.READ): probatio.In(
        EnableOptions
    ),
    probatio.Optional(CONF_ALTERNATE_EMAIL): cv.string,
}

CHAT_SERVICE_SEND_MESSAGE_SCHEMA = {
    probatio.Required(ATTR_CHAT_ID): cv.string,
    probatio.Required(ATTR_MESSAGE): cv.string,
    probatio.Optional(ATTR_CONTENT_TYPE, default="text"): probatio.In(CONTENT_TYPES),
}

STATUS_SERVICE_UPDATE_USER_STATUS_SCHEMA = {
    probatio.Required(ATTR_AVAILABILITY): probatio.Coerce(Availability),
    probatio.Required(ATTR_ACTIVITY): probatio.Coerce(Activity),
    probatio.Optional(ATTR_EXPIRATIONDURATION): cv.string,
}

STATUS_SERVICE_UPDATE_USER_PERERRED_STATUS_SCHEMA = {
    probatio.Required(ATTR_AVAILABILITY): probatio.Coerce(PreferredAvailability),
    probatio.Optional(ATTR_EXPIRATIONDURATION): cv.string,
}
