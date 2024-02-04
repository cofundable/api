"""Test package level details about the cofundable api package."""

import cofundable


def test_package_is_imported_with_correct_name():
    """The api package should be imported with the correct name."""
    assert cofundable.__name__ == "cofundable"
