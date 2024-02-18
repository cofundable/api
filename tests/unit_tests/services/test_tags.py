"""Test the cofundable.services.tags module."""

from sqlalchemy.orm import Session

from cofundable.services.tags import tag_service


class TestGetTagsByName:
    """Test the TagsCRUD.get_tags_by_name() method."""

    def test_return_all_tags_if_they_exist(self, test_session: Session):
        """If all tags exist, all tags should be returned."""
        # setup
        tag_names = ["a", "b", "c"]
        # execution
        tags = tag_service.get_tags_by_name(
            db=test_session,
            tag_names=tag_names,
        )
        # validation - Check that all three tags have a match
        assert len(tags) == 3
        assert set(tag_names) == {tag.name for tag in tags}

    def test_return_only_the_tags_that_exist(self, test_session: Session):
        """Only the tags that already exist should be returned."""
        # setup
        tag_names = ["a", "b", "z"]
        # execution
        tags = tag_service.get_tags_by_name(
            db=test_session,
            tag_names=tag_names,
        )
        # validation - Check that only the first two tags have a match
        assert len(tags) == 2
        assert set(tag_names[:2]) == {tag.name for tag in tags}

    def test_return_empty_list_if_no_tags_exist(self, test_session: Session):
        """If no matching tags exist, an empty list should be returned."""
        # setup
        tag_names = ["x", "y", "z"]
        # execution
        tags = tag_service.get_tags_by_name(
            db=test_session,
            tag_names=tag_names,
        )
        # validation - Check that an empty list is returned
        assert tags == set()


class TestGetOrCreateTagsByName:
    """Test the TagsCRUD.get_or_create_tags_by_name() method."""

    def test_do_not_create_any_records_if_all_tags_exist(
        self,
        test_session: Session,
    ):
        """If all tags already exist don't create any more records."""
        # setup - confirm all tags exist
        tag_names = ["a", "b", "c"]
        tags_old = set(tag_service.get_all(test_session))
        assert set(tag_names) == {tag.name for tag in tags_old}
        # execution
        tags_out = tag_service.get_or_create_tags_by_name(
            db=test_session,
            tag_names=tag_names,
        )
        tags_new = set(tag_service.get_all(test_session))
        # validation - Check that no new tags were created
        assert len(tags_new) == len(tags_old)
        assert tags_old == tags_out
        assert tags_new == tags_out

    def test_create_new_records_if_tag_does_not_exist(
        self,
        test_session: Session,
    ):
        """If a tag doesn't exist, it should be created and returned with the rest."""
        # setup - confirm the z tag doesn't exist
        missing = "z"
        tag_names = ["a", "b", missing]
        tags_old = set(tag_service.get_all(test_session))
        assert missing not in {tag.name for tag in tags_old}
        # execution
        tags_out = tag_service.get_or_create_tags_by_name(
            db=test_session,
            tag_names=tag_names,
        )
        tags_new = set(tag_service.get_all(test_session))
        # validation - Check that a new tag was created
        assert len(tags_new) > len(tags_old)
        # validation - Check that newly created tags are also returned
        assert len(tags_out) == 3
        assert tags_out.issubset(tags_new)
        assert missing in {tag.name for tag in tags_out}
