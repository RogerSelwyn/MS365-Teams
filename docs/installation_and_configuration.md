---
title: Installation and Configuration
nav_order: 4
---

# Installation and Configuration
This page details the configuration details for this integration. General instructions can be found on the MS365 Home Assistant [Installation and Configuration](https://rogerselwyn.github.io/MS365-HomeAssistant/installation_and_configuration.html) page.

### Configuration variables

Key | Type | Required | Description
-- | -- | -- | --
`account_name` | `string` | `True` | Uniquely identifying name for the account. Entity names will be suffixed with this. Do not use email address or spaces.
`client_id` | `string` | `True` | Client ID from your Entra ID App Registration.
`environment_secret` | `boolean` | `True` | If True (**default is False**) uses client secret from environment variable defined by `client_sec_variable`. If False uses client secret entered by config dialogue.
`client_secret` | `string` | `True` | Client Secret from your Entra ID App Registration. Used if `environment_secret` is False.
`client_sec_variable` | `string` | `True` | Defines the environment variable the client secret is stored in. Used if `environment_secret` is True.
`alt_auth_method` | `boolean` | `False` | If False (default), authentication is not dependent on internet access to your HA instance. [See Authentication](./authentication.md)
`chat_enable` | `string` | `False` | Disabled, **Read**, Update - Enable or disable chat sensor
`status_enable` | `string` | `False` | Disabled, **Read**, Update - Enable or disable status sensor
`alternate_email` | `string` | `False` | Email address to monitor status for. `status_enable` must be `Read`

#### Advanced API Options

These options will only be relevant for users in very specific circumstances.

Key | Type | Required | Description
-- | -- | -- | --
`country` | `string` | `True` | Selection of an alternate country specific API. Currently only 21Vianet from China and MS365 GCC.
`tenant_id` | `string` | `False` | Azure tenant ID for single-tenant app registrations. Leave blank for multi-tenant apps.

### Options variables

Key | Type | Required | Description
-- | -- | -- | --
`update_interval` | `int` | `False` | The update interval for the status and chat sensors in seconds. Default 30, Min 1, Max 60.
