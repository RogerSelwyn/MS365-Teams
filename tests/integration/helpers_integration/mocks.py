"""Mock setup."""

# from datetime import timedelta

from ...helpers.utils import mock_call  # utcnow
from ..const_integration import URL


class MS365Mocks:
    """Standard mocks."""

    def standard_mocks(self, requests_mock):
        """Setup the standard mocks."""
        mock_call(requests_mock, URL.ME, "me")
        mock_call(requests_mock, URL.CHATS, "chats")
        mock_call(requests_mock, URL.CHAT1_MESSAGES, "chat1_messages")
        mock_call(requests_mock, URL.CHAT1_MEMBERS, "chat1_members")
        mock_call(requests_mock, URL.CHAT2_MESSAGES, "chat2_messages")
        mock_call(requests_mock, URL.CHAT2_MEMBERS, "chat2_members")
        mock_call(requests_mock, URL.PRESENCE, "presence")
        mock_call(requests_mock, URL.ALTERNATE_USER, "alternate_user")
        mock_call(requests_mock, URL.ALTERNATE_PRESENCE, "alternate_presence")


MS365MOCKS = MS365Mocks()
