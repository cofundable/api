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


# accounts
ACCOUNT_ACME = uuid5(namespace, "acme-account")
ACCOUNT_AID = uuid5(namespace, "mutual-aid-account")
ACCOUNT_ALICE = uuid5(namespace, "alice-account")
ACCOUNT_BOB = uuid5(namespace, "bob-account")
ACCOUNTS = {
    ACCOUNT_ACME: {
        "name": "acme",
        "balance": 5,
    },
    ACCOUNT_AID: {
        "name": "mutual-aid",
        "balance": 0,
    },
    ACCOUNT_ALICE: {
        "name": "alice",
        "balance": 10,
    },
    ACCOUNT_BOB: {
        "name": "bob",
        "balance": 5,
    },
}

# causes
ACME = uuid5(namespace, "acme")
MUTUAL_AID = uuid5(namespace, "mutual-aid")
CAUSES = {
    ACME: {
        "name": "Acme",
        "handle": "acme",
        "description": "Local organization",
        "account_id": ACCOUNT_ACME,
    },
    MUTUAL_AID: {
        "name": "Mutual aid group",
        "handle": "mutual-aid",
        "description": "Local organization",
        "account_id": ACCOUNT_AID,
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
        "handle": "alice",
        "name": "Alice Williams",
        "bio": "Bio for Alice",
        "account_id": ACCOUNT_ALICE,
    },
    BOB: {
        "handle": "bob",
        "name": "Bob Johnson",
        "account_id": ACCOUNT_BOB,
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
        "user_id": BOB,
    },
}

# records to create and insert directly
UUID_TABLES = {
    "cause": MockTableData(model=Cause, records=CAUSES),
    "tag": MockTableData(model=Tag, records=TAGS),
    "user": MockTableData(model=User, records=USERS),
    "bookmark": MockTableData(model=Bookmark, records=BOOKMARKS),
}
