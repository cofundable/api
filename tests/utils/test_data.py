"""Create test data for the mock database."""

from uuid import uuid4, uuid5

namespace = uuid4()

# causes
ACME = uuid5(namespace, "Acme")
MUTUAL_AID = uuid5(namespace, "mutual aid")
CAUSES = {
    ACME: {
        "id": ACME,
        "name": "Acme",
        "handle": "acme",
        "description": "Local organization",
    },
    MUTUAL_AID: {
        "id": MUTUAL_AID,
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
    TAG_A: {
        "id": TAG_A,
        "name": "a",
    },
    TAG_B: {
        "id": TAG_B,
        "name": "b",
    },
    TAG_C: {
        "id": TAG_C,
        "name": "c",
    },
}

# cause tags
CAUSE_TAGS = {
    ACME: [TAG_A, TAG_B],
    MUTUAL_AID: [TAG_B, TAG_C],
}
