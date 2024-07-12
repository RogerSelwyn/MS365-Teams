---
title: Services
nav_order: 15
---

# Services

## Chat Services

These services must be targeted at a `chat` sensor. 

### ms365_teams.send_chat_message
Send message to specified chat - All parameters are shown in the available parameter list on the Developer Tools/Services tab.

#### Example send chat message service call

```yaml
service: ms365_teams.send_chat_message
target:
  entity_id: sensor.roger_chats
data:
  chat_id: xxxxxxxxxxxxxxxxxxxxxxxxx
  message: Hello world
  content_type: text
```

## Status Services

These services must be targeted at a `status` sensor. They can only target the logged-in user's status.

### ms365_teams.update_user_status
Update Teams status for the logged in client. This will not override a status that is set via the MS Teams client. Allowable pairings of availability and activity are show in the [MS Graph Documentation](https://learn.microsoft.com/en-us/graph/api/presence-setpresence?view=graph-rest-1.0&tabs=http#request-body). The expiration/duration field is also documented on the same page. It defaults to 5 minutes.

#### Example update user status service call

```yaml
service: ms365_teams.update_user_status
data:
  availability: Busy
  activity: InACall
  expiration_duration: PT1H
target:
  entity_id: sensor.roger_teams_status
```
### ms365_teams.update_user_preferred_status
Update Teams preferred status for the logged-in user. This is equivalent to setting status within the Teams client. Allowable pairings of availability and activity are show in the [MS Graph Documentation](https://learn.microsoft.com/en-us/graph/api/presence-setuserpreferredpresence?view=graph-rest-1.0&tabs=http#request-body). The expiration/duration field is also documented on the same page. If not provided, a default expiration will be applied: DoNotDisturb or Busy - Expiration in 1 day; All others - Expiration in 7 days

#### Example update user preferred status service call

```yaml
service: ms365_teams.update_user_preferred_status
data:
  availability: Offline
  expiration_duration: PT1H
target:
  entity_id: sensor.roger_teams_status
```