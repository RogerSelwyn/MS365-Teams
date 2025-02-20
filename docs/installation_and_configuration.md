---
title: Installation and Configuration
nav_order: 4
---

# Installation and Configuration
## Installation
1. Ensure you have followed the [prerequisites instructions](./prerequisites.md)
    * Ensure you have a copy of the Client ID and the Client Secret **Value** (not the ID)
1. Optionally you can set up the [permissions](./permissions.md), alternatively you will be requested to approve permissions when you authenticate to MS 365.
1. Install this integration:
    * Recommended - see below, or
    * Manually - Copy [these files](https://github.com/RogerSelwyn/MS365-Teams/tree/main/custom_components/ms365_teams) to custom_components/ms365_teams/.
1. Restart your Home Assistant instance to enable the integration
1. Add the integration via the `Devices & Services` dialogue. Follow the instructions in the install process (or see [Authentication](./authentication.md)) to establish the link between this integration and the Entra ID App Registration
    * A persistent token will be created in the hidden directory config/ms365_storage/.MS365-token-cache

**Note** If your installation does not complete authentication, or the sensors are not created, please go back and ensure you have accurately followed the steps detailed, also look in the logs to see if there are any errors. You can also look at the [errors page](./errors.md) for some other possibilities.

**Note** To configure a second account, add the integration again via the `Devices & Services` dialogue.

### HACS

1. Launch HACS
1. Navigate to the Integrations section
1. Add this repository as a Custom Repository (Integration) via the menu at top right.
1. Search for "Microsoft 365 To Do"
1. Select "Install this repository"
1. Restart Home Assistant


### Configuration variables

Key | Type | Required | Description
-- | -- | -- | --
`account_name` | `string` | `True` | Uniquely identifying name for the account. Entity names will be suffixed with this. Do not use email address or spaces.
`client_id` | `string` | `True` | Client ID from your Entra ID App Registration.
`client_secret` | `string` | `True` | Client Secret from your Entra ID App Registration.
`alt_auth_method` | `boolean` | `False` | If False (default), authentication is not dependent on internet access to your HA instance. [See Authentication](./authentication.md)
`chat_enable` | `string` | `False` | Disabled, **Read**, Update - Enable or disable chat sensor
`status_enable` | `string` | `False` | Disabled, **Read**, Update - Enable or disable status sensor
`alternate_email` | `string` | `False` | Email address to monitor status for. `status_enable` must be `Read`

### Options variables

Key | Type | Required | Description
-- | -- | -- | --
`update_interval` | `int` | `False` | The update interval for the status and chat sensors in seconds. Default 30, Min 1, Max 60.