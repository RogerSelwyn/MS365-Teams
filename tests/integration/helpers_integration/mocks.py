"""Mock setup."""

# from datetime import timedelta

from ...helpers.utils import mock_call, load_json
from ..const_integration import CN21VURL, URL


class MS365Mocks:
    """Standard mocks."""

    def cn21v_mocks(self, requests_mock, tenant_id="common"):
        """Setup the standard mocks."""
        mock_call(requests_mock, CN21VURL.DISCOVERY, "discovery")
        # Mock the /common/ openid config with CN21V-specific URLs.
        # MSAL fetches this via the discovery response's tenant_discovery_endpoint.
        openid_data = load_json("O365/openid.json")
        openid_data = openid_data.replace(
            "login.microsoftonline.com",
            "login.partner.microsoftonline.cn",
        )
        url = CN21VURL.OPENID.value.replace("common", tenant_id)
        requests_mock.get(url, text=openid_data)
        mock_call(requests_mock, CN21VURL.ME, "me")
        mock_call(requests_mock, CN21VURL.CHATS, "chats")
        mock_call(requests_mock, CN21VURL.CHAT1_MESSAGES, "chat1_messages")
        mock_call(requests_mock, CN21VURL.PRESENCE, "presence")

    def standard_mocks(self, requests_mock):
        """Setup the standard mocks."""
        mock_call(requests_mock, URL.OPENID, "openid")
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
