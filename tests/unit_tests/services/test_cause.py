"""Test cofundable.services.causes code."""

from uuid import UUID

from cofundable.schemas.cause import CauseRequestSchema
from cofundable.services.causes import create_cause, list_causes


class TestCreateCause:
    """Test create_cause()."""

    def test_id_should_be_automatically_set(self):
        """The id should be automatically set using uuid4()."""
        # setup
        cause_data = CauseRequestSchema(
            name="Acme",
            description="Test description",
            handle="acme",
        )
        # execution
        cause_output = create_cause(data=cause_data)
        # validation
        assert cause_output.id is not None
        assert isinstance(cause_output.id, UUID)


class TestListCauses:
    """Test list_causes()."""

    def test_return_all_causes_by_default(self):
        """If no filters are passed, then all causes should be returned."""
        # execution
        causes = list_causes()
        # validation
        assert len(causes) == 1
