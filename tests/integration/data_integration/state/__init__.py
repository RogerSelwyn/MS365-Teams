# pylint: disable=line-too-long
"""Tests for MS365 Mail."""

UPDATE_CHATS = data = [
    {
        "chat_id": "chat1",
        "chat_type": "oneOnOne",
        "members": "John Doe,Jane Doe",
    },
    {
        "chat_id": "chat2",
        "chat_type": "group",
        "members": "John Doe,jane@nomail.com,Name Unknown",
        "topic": None,
    },
]
