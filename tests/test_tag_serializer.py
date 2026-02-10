"""Tests for tag serialization round-trip."""

from hypothesis import given, settings, strategies as st

from src.tag_serializer import (
    serialize_ec2_tags, deserialize_ec2_tags,
    serialize_s3_tags, deserialize_s3_tags,
    serialize_arn_tags, deserialize_arn_tags,
)

# Strategy: tag payload with non-empty string keys and string values
tag_key = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_:./ "),
    min_size=1, max_size=64,
)
tag_value = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_:/.@ "),
    min_size=0, max_size=128,
)
tag_payload = st.dictionaries(tag_key, tag_value, min_size=1, max_size=10)

SERIALIZER_PAIRS = [
    (serialize_ec2_tags, deserialize_ec2_tags),
    (serialize_s3_tags, deserialize_s3_tags),
    (serialize_arn_tags, deserialize_arn_tags),
]


# Feature: auto-tag-resources, Property 3: Tag serialization round-trip
@settings(max_examples=100)
@given(tags=tag_payload)
def test_tag_serialization_round_trip(tags):
    """Property 3: Tag serialization round-trip.

    For any Tag Payload, serializing then deserializing with any
    service serializer pair produces a dict equal to the original.
    **Validates: Requirements 13.1, 13.2, 13.3, 13.4, 13.5, 13.6**
    """
    for serialize, deserialize in SERIALIZER_PAIRS:
        serialized = serialize(tags)
        assert isinstance(serialized, list)
        for item in serialized:
            assert "Key" in item and "Value" in item
        deserialized = deserialize(serialized)
        assert deserialized == tags
