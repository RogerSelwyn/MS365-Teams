---
title: Permissions
nav_order: 3
---

# Permissions

This page details the permissions for this integration. General instructions can be found on the MS365 Home Assistant [Permissions](https://rogerselwyn.github.io/MS365-HomeAssistant/permissions.html) page.

   | Feature  | Permissions                | Update | MS Graph Description                                           | Notes |
   |----------|----------------------------|:------:|----------------------------------------------------------------|-------|
   | All      | offline_access             |        | *Maintain access to data you have given it access to*          |       |
   | All      | User.Read                  |        | *Sign in and read user profile*                                |       |
   | Chat     | Chat.Read                  |        | *Read user chat messages*                                      | Not for personal accounts/shared mailboxes |
   | Chat     | Chat.ReadWrite             | Y      | *Read and write user chat messages*                            | Not for personal accounts/shared mailboxes |
   | Status   | Presence.Read              |        | *Read user's presence information*                             | Not for personal accounts/shared mailboxes |
   | Status   | Presence.ReadWrite         | Y      | *Read and write a user's presence information*                 | Not for personal accounts/shared mailboxes |
   | Status   | Presence.Read.All          |        | *Read presence information of all users in your organization*  | Used if you want to monitor another user's status. Not for personal accounts/shared mailboxes |
   | Status   | User.ReadBasic.All         |        | *Read all users' basic profiles*                               | Used if you want to monitor another user's status. Not for personal accounts/shared mailboxes |
   
