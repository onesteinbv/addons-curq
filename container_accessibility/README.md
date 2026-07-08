# CURQ Accessibility

## Restricted Group

The restricted group is a special group that is used to restrict access to certain
features and settings in CURQ. The group is introduced to limit the access to
destructive actions and standardize CURQ configuration, without it users with
`base.group_system` would have unrestricted access. E.g. users with `base.group_system`
can edit, or remove `ir.ui.views`, `ir.actions`, `ir.model.access`, and many more, which
can lead to unstandardized configurations and even incorrect functioning of CURQ. By
using the restricted group, we can ensure that only users that are used for maintenance
have access to these features, while customers, support employees, and consultants do
not have access to these features.

**Restricted users cannot**:

- Edit or remove `ir.ui.views`, `ir.actions`, `ir.model.access`, `res.groups`, and many
  more.
- Create unrestricted users.
- See unrestricted users in the user list.
- CRUD private oauth providers and mail servers
- Install, upgrade, or uninstall modules that are not bundles (`_install` modules)

## Removal of "become superuser"

Some features should not even be accessible to administrators, the "become superuser"
feature is outright removed, which allows administrators to become the superuser aka
`base.user_root`. To ensure accountability, this module adds immutable audit log rules
that track potential malicious violations of privacy rules. For example, if a support
user exports contact information, this action will be logged and cannot be deleted, even
by administrators / maintainers.

## Private oauth provider, and mail servers

Restricted users cannot access private OAuth providers, which are reserved for support
employees and partners to use as single sign-on. While customers can add their own OAuth
providers, private ones are restricted to prevent accidental lockouts of support and
partner accounts. Mail servers are also restricted to prevent customers from modifying
the mail server configuration, which could disrupt email functionality and generate
unnecessary support requests.

## User Roles

These are the user roles in CURQ:

`Administrator`: has full access to all features and settings of CURQ.

`Manager`: doesn't have access to system altering configurations, but can e.g. update
company information, change document layouts, and configure mail servers. Can create
users but not Administrators.

`Accountant`: has access to accounting features

`User`: has access to their own documents (tasks, projects, etc.), but cannot change any
settings or create users.

`Guest`: portal user

To limit access to certain configuration options, the module uses...

All groups are assigned here instead of in the corresponding modules, to avoid having to
change the groups in multiple places when we want to change the access rights of a role.
This makes it easier to maintain the access rights of the roles. Groups are assigned to
the roles as they are created.

This also enforces the use of the roles, as users cannot be assigned to groups directly,
but only to roles. This makes it easier to manage the access rights of users, and the
access rights of that role are defined in one place.

Normally with `base_user_role` the user can have multiple roles at the same time,
furthermore you can assign a start and end date for each role, but in CURQ we want to
have a simplified role system, where each user can only have one role.

To ensure the managers cannot assign themselves the Administrator role, we have...

User limit functionality is also implemented, which allows us to limit the number of
users that can be created in the system. This will only check the number of users that
are assigned to the `Manager`, `User`, or `Accountant` role.

Partners related to users with `Administrator` or no role will be hidden for users with
the `Manager`, `User`, or `Accountant` role.

The default user template is not altered because that will also affect `base.user_admin`
and will overall lead to implicit behaviour.

## Roadmap

Can we get rid of the `group_restricted` group and instead purely use the roles to
restrict access? This would simplify the access rights management, but it would also
require a lot of changes to the existing codebase. We need to evaluate if this is
feasible and if it would be worth the effort.
