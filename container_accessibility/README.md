# CURQ Accessibility

These are the user roles in CURQ:

`Administrator`: has full access to all features and settings of CURQ.

`Manager`: doesn't have access to system altering configurations, but can e.g. update company information, change document layouts, and configure mail servers. Can create users but not Administrators.

`User`: has access to his or her own documents (tasks, projects, etc.), but cannot change any settings or create users.

`Guest`: portal user

To limit access to certain configuration options, the module uses...

All groups are assigned here instead of in the corresponding modules, to avoid having to change the groups in multiple places when we want to change the access rights of a role. This makes it easier to maintain the access rights of the roles. Groups are assigned to the roles as they are created.

This also enforces the use of the roles, as users cannot be assigned to groups directly, but only to roles. This makes it easier to manage the access rights of users, as they can only be assigned to one role, and the access rights of that role are defined in one place.
