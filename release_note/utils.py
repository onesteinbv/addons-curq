def version_to_tuple(version):
    """Converts a version string like 'v1.2.3' to a tuple (1, 2, 3) for easy comparison.
    If the version string is invalid, returns (0, 0, 0).
    """
    if not version:
        return (0, 0, 0)

    try:
        return tuple(int(part) for part in version.removeprefix("v").split("."))
    except ValueError:
        return (0, 0, 0)
