"""Tests for tag builder."""

from hypothesis import given, settings, strategies as st

from src.tag_builder import build_tags

EXPECTED_KEYS = {"Owner", "CreatedBy", "CreationDate"}

tag_value = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_:/.@ "),
    min_size=1, max_size=128,
)


# Feature: auto-tag-resources, Property 2: Tag builder completeness and correctness
@settings(max_examples=100)
@given(
    owner=tag_value,
    arn=tag_value,
    event_time=tag_value,
    environment=tag_value,
    project=tag_value,
)
def test_tag_builder_completeness_and_correctness(owner, arn, event_time, environment, project):
    """Property 2: Tag builder completeness and correctness.

    For any combination of inputs, build_tags returns a dict containing exactly
    the three standard keys with the correct values.
    **Validates: Requirements 12.1, 12.2, 12.3**
    """
    tags = build_tags(owner, arn, event_time, environment, project)

    assert set(tags.keys()) == EXPECTED_KEYS
    assert tags["Owner"] == owner
    assert tags["CreatedBy"] == arn
    assert tags["CreationDate"] == event_time
