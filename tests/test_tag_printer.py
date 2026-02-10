"""Tests for tag printer/parser round-trip."""

from hypothesis import given, settings, strategies as st

from src.tag_printer import print_tags, parse_tags

# Keys and values must not contain '=' or ',' per the design doc constraint
safe_char = st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_:/.@ ")
tag_key = st.text(alphabet=safe_char, min_size=1, max_size=64).filter(
    lambda s: "=" not in s and "," not in s
)
tag_value = st.text(alphabet=safe_char, min_size=1, max_size=128).filter(
    lambda s: "=" not in s and "," not in s
)
tag_payload = st.dictionaries(tag_key, tag_value, min_size=1, max_size=10)


# Feature: auto-tag-resources, Property 4: Tag printer/parser round-trip
@settings(max_examples=100)
@given(tags=tag_payload)
def test_tag_printer_parser_round_trip(tags):
    """Property 4: Tag printer/parser round-trip.

    For any Tag Payload with keys/values not containing '=' or ',',
    parse_tags(print_tags(payload)) produces a dict equal to the original.
    **Validates: Requirements 14.2, 14.3**
    """
    printed = print_tags(tags)
    assert isinstance(printed, str)
    parsed = parse_tags(printed)
    assert parsed == tags
