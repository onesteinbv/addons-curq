Shows a user-facing release note dialog after an update.

This module automatically shows a popup with release notes when a user logs in
after a new version has been deployed. Each user's last read version is tracked,
so the popup only appears once per version.

**towncrier integration**

The module is designed to work with `towncrier
<https://towncrier.readthedocs.io/>`_. Configure towncrier to produce Markdown
output and commit the result as ``NEWS.md`` in the root of your repository.

**Extending**

Inherit ``release.note.wizard`` and override ``_get_release_notes()`` to
retrieve the changelog from a different source, or ``_parse_release_notes()``
to change the parsing logic.
