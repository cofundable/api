import api


def test_package_is_imported_with_correct_name():
    """The api package should be imported with the correct name"""
    assert api.__name__ == "api"
