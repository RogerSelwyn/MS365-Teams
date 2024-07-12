---
title: Permissions
nav_order: 3
---

# Permissions

Under "API Permissions" click Add a permission, then Microsoft Graph, then Delegated permission, and add the permissions as detailed in the list and table below:

   | Feature  | Permissions                | Update | MS Graph Description                                           | Notes |
   |----------|----------------------------|:------:|----------------------------------------------------------------|-------|
   | All      | offline_access             |        | *Maintain access to data you have given it access to*          |       |
   | All      | User.Read                  |        | *Sign in and read user profile*                                |       |
   | Chat     | Chat.Read                  |        | *Read user chat messages*                                      | Not for personal accounts/shared mailboxes |
   | Chat     | Chat.ReadWrite             | Y      | *Read and write user chat messages*                            | Not for personal accounts/shared mailboxes |
   | Status   | Presence.Read              |        | *Read user's presence information*                             | Not for personal accounts/shared mailboxes |
   | Status   | Presence.ReadWrite         | Y      | *Read and write a user's presence information*                 | Not for personal accounts/shared mailboxes |
   | Status   | Presence.Read.All          |        | *Read presence information of all users in your organization*  | Used if you want to monitor another user's status. Not for personal accounts/shared mailboxes |
   

## Changing Features and Permissions
If you decide to enable new features in the integration, or decide to change from read only to read/write, you will very likely get a warning message similar to the following in your logs.

`Minimum required permissions not granted: ['Tasks.Read', ['Tasks.ReadWrite']]`

You will need to delete as detailed on the [token page](./token.md)
