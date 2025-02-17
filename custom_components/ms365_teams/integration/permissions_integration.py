"""Permissions processes for mail."""

from copy import deepcopy

from ..classes.permissions import BasePermissions
from ..const import PERM_BASE_PERMISSIONS
from .const_integration import (
    CONF_ALTERNATE_EMAIL,
    CONF_CHAT_ENABLE,
    CONF_STATUS_ENABLE,
    PERM_CHAT_READ,
    PERM_CHAT_READWRITE,
    PERM_PRESENCE_READ,
    PERM_PRESENCE_READ_ALL,
    PERM_PRESENCE_READWRITE,
    PERM_USER_READBASIC_ALL,
    EnableOptions,
)


class Permissions(BasePermissions):
    """Class in support of building permission sets."""

    def __init__(self, hass, config, token_backend):
        """Initialise the class."""
        super().__init__(hass, config, token_backend)

        self._chat_enable = self._config.get(CONF_CHAT_ENABLE)
        self._status_enable = self._config.get(CONF_STATUS_ENABLE)
        self._alternate_email = self._config.get(CONF_ALTERNATE_EMAIL, None)

    @property
    def requested_permissions(self):
        """Return the required scope."""
        if not self._requested_permissions:
            self._requested_permissions = deepcopy(PERM_BASE_PERMISSIONS)
            self._build_chat_permissions()
            self._build_status_permissions()

        return self._requested_permissions

    def _build_status_permissions(self):
        if self._status_enable == EnableOptions.UPDATE:
            self._requested_permissions.append(PERM_PRESENCE_READWRITE)
        elif self._status_enable == EnableOptions.READ or self._alternate_email:
            self._requested_permissions.append(PERM_PRESENCE_READ)
        if self._alternate_email:
            self._requested_permissions.append(PERM_PRESENCE_READ_ALL)
            self._requested_permissions.append(PERM_USER_READBASIC_ALL)

    def _build_chat_permissions(self):
        if self._chat_enable == EnableOptions.UPDATE:
            self._requested_permissions.append(PERM_CHAT_READWRITE)
        elif self._chat_enable == EnableOptions.READ:
            self._requested_permissions.append(PERM_CHAT_READ)
