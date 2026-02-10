"""Tests for identity extraction."""

import pytest
from hypothesis import given, settings, strategies as st

from src.identity import extract_owner


# --- Hypothesis strategies ---

def iam_user_identity():
    """Generate valid IAMUser userIdentity dicts."""
    return st.fixed_dictionaries({
        "type": st.just("IAMUser"),
        "userName": st.text(
            alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_@."),
            min_size=1, max_size=64
        ),
        "arn": st.text(min_size=1),
    })


def assumed_role_identity():
    """Generate valid AssumedRole userIdentity dicts with a realistic ARN."""
    return st.builds(
        lambda role_name, session_name: {
            "type": "AssumedRole",
            "arn": f"arn:aws:sts::123456789012:assumed-role/{role_name}/{session_name}",
        },
        role_name=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
            min_size=1, max_size=32
        ),
        session_name=st.text(
            alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_@."),
            min_size=1, max_size=64
        ),
    )


def root_identity():
    """Generate Root userIdentity dicts."""
    return st.fixed_dictionaries({
        "type": st.just("Root"),
        "arn": st.just("arn:aws:iam::123456789012:root"),
    })


def federated_user_identity():
    """Generate FederatedUser userIdentity dicts."""
    return st.fixed_dictionaries({
        "type": st.just("FederatedUser"),
        "userName": st.text(
            alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_@."),
            min_size=1, max_size=64
        ),
    })


def unknown_identity():
    """Generate unrecognized or missing identity dicts."""
    return st.one_of(
        st.just({}),
        st.just(None),
        st.fixed_dictionaries({"type": st.text(min_size=1).filter(
            lambda t: t not in ("IAMUser", "AssumedRole", "Root", "FederatedUser")
        )}),
    )


# --- Property test ---
# Feature: auto-tag-resources, Property 1: Identity extraction correctness

@settings(max_examples=100)
@given(identity=st.one_of(
    iam_user_identity(),
    assumed_role_identity(),
    root_identity(),
    federated_user_identity(),
    unknown_identity(),
))
def test_identity_extraction_correctness(identity):
    """Property 1: Identity extraction correctness.

    For any valid userIdentity dict with a recognized type, extract_owner
    returns the correct owner name.
    **Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5**
    """
    result = extract_owner(identity)
    assert isinstance(result, str)
    assert len(result) > 0

    if identity is None or not isinstance(identity, dict):
        assert result == "Unknown"
        return

    identity_type = identity.get("type", "")

    if identity_type == "IAMUser":
        assert result == identity["userName"]
    elif identity_type == "AssumedRole":
        arn = identity.get("arn", "")
        expected = arn.rsplit("/", 1)[-1] if arn and "/" in arn else "Unknown"
        assert result == expected
    elif identity_type == "Root":
        assert result == "root"
    elif identity_type == "FederatedUser":
        assert result == identity["userName"]
    else:
        assert result == "Unknown"


# --- Unit tests for edge cases ---

def test_root_returns_root():
    """Requirement 11.3: Root type returns 'root'."""
    assert extract_owner({"type": "Root"}) == "root"


def test_missing_user_identity_returns_unknown():
    """Requirement 11.5: Missing userIdentity returns 'Unknown'."""
    assert extract_owner(None) == "Unknown"
    assert extract_owner({}) == "Unknown"


def test_malformed_arn_assumed_role():
    """Requirement 11.5: AssumedRole with no '/' in ARN returns 'Unknown'."""
    assert extract_owner({"type": "AssumedRole", "arn": "no-slash-here"}) == "Unknown"
    assert extract_owner({"type": "AssumedRole", "arn": ""}) == "Unknown"
    assert extract_owner({"type": "AssumedRole"}) == "Unknown"
