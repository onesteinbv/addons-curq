# Contributing

## News Fragments

For every user-facing change, add a Towncrier news fragment.

### When to add a fragment

Add a fragment when your change affects what end users see or do, for example:

- New functionality
- Behavior changes or improvements
- Bug fixes visible to users

If a change is only internal and has no user impact, a fragment is not necessary.

### Where to add it

Create the file in `newsfragments/`.

### File naming

Use:

`<identifier>.<type>.md`

- Use the PR number when available, for example `123.fix.md`.
- If there is no PR number, use any unique identifier, for example `+123.misc.md`.

### Allowed types

- `feat`
- `imp`
- `fix`
- `misc`

### Writing guidelines

Write short, user-facing text (1 to 2 sentences) that explains the outcome for end users.

- Focus on what changed for the user, not internal implementation details.
- Keep wording clear and practical.
- Avoid technical jargon or internal references.
- Avoid markdown structures like headings, lists, or code blocks.

Examples:

- "Added automatic assignment of incoming payments to open invoices."
- "Fixed duplicate contact suggestions when creating a sales order."

Fragments are compiled into `NEWS.md` during the release process.
