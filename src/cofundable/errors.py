"""Create custom errors for the Cofundable API."""


class CauseHandleNotFoundError(Exception):
    """
    No cause was found with the handle provided.

    Attributes
    ----------
    handle: str
        The handle that was used to try to find a cause in the database

    """

    def __init__(self, handle: str) -> None:
        """Init the CauseHandleNotFoundError."""
        super().__init__()
        self.handle = handle
