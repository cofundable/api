"""Create test data for the mock database."""

from dataclasses import dataclass
from uuid import UUID, uuid4, uuid5

from cofundable.models import (
    UUIDAuditBase,
    Bookmark,
    Cause,
    Tag,
    User,
)

namespace = uuid4()


@dataclass
class MockTableData:
    """Map test data to the model used to populate that test data in the db."""

    model: type[UUIDAuditBase]
    records: dict[UUID, dict]


# causes
ACME = uuid5(namespace, "Acme")
MUTUAL_AID = uuid5(namespace, "mutual aid")
CAUSES = {
    ACME: {
        "name": "Acme",
        "handle": "acme",
        "description": "Local organization",
    },
    MUTUAL_AID: {
        "name": "Mutual aid group",
        "handle": "mutual-aid",
        "description": "Local organization",
    },
}

# tags
TAG_A = uuid5(namespace, "a")
TAG_B = uuid5(namespace, "b")
TAG_C = uuid5(namespace, "c")
TAGS = {
    TAG_A: {"name": "a"},
    TAG_B: {"name": "b"},
    TAG_C: {"name": "c"},
}

# cause tags
CAUSE_TAGS = {
    ACME: [TAG_A, TAG_B],
    MUTUAL_AID: [TAG_B, TAG_C],
}


# users
ALICE = uuid5(namespace, "alice")
BOB = uuid5(namespace, "bob")
USERS = {
    ALICE: {
        "username": "alice",
        "name": "Alice Williams",
        "bio": "Bio for Alice",
    },
    BOB: {
        "username": "bob",
        "name": "Bob Johnson",
    },
}

# bookmarks
ALICE_ACME = uuid5(namespace, "alice<>acme")
BOB_ACME = uuid5(namespace, "bob<>acme")
BOOKMARKS = {
    ALICE_ACME: {
        "cause_id": ACME,
        "user_id": ALICE,
    },
    BOB_ACME: {
        "cause_id": ACME,
        "user_id": ALICE,
    },
}

# records to create and insert directly
UUID_TABLES = {
    "cause": MockTableData(model=Cause, records=CAUSES),
    "tag": MockTableData(model=Tag, records=TAGS),
    "user": MockTableData(model=User, records=USERS),
    "bookmark": MockTableData(model=Bookmark, records=BOOKMARKS),
}
