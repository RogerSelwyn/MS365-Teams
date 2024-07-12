---
title: Events
nav_order: 16
---

# Events

The attribute `ha_event` shows whether the event is triggered by an HA initiated action

##  Teams Status Events

Events will be raised for the following items.

- ms365_teams_update_user_status - User teams presence updated
- ms365_teams_update_user_preferred_status - User teams preferred presence updated

The events have the following general structure:

```yaml
event_type: ms365_teams_update_user_status
data:
  name: Joe Teams Status
  status:
    availability: Available
    activity: Available
  ha_event: true
origin: LOCAL
time_fired: "2024-02-12T18:22:36.694771+00:00"
context:
  id: 01HPF8X14PYZ1QRZ8V199JSQTQ
  parent_id: null
  user_id: null
```

##  Teams Chat Events

Events will be raised for the following items.

- ms365_teams_send_chat_message - Message sent to specified chat via the MS365 integration

The events have the following general structure:

```yaml
event_type: ms365_teams_send_chat_message
data:
  chat_id: >-
    19:5f6d6952-ace3-9999-9999-14af19704e05_99999999-a5c7-46da-8107-b25090a1ed66@unq.gbl.spaces
  ha_event: true
origin: LOCAL
time_fired: "2023-06-07T17:43:39.509758+00:00"
context:
  id: 01H2BFA0QNCGEN2ZYRWGBFFHRF
  parent_id: null
  user_id: null
```