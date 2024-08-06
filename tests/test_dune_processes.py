"""Tests for the main module."""

from dune_processes import __version__


def test_version():
    """Check that the version is acceptable."""
    assert __version__ == "0.1.0"
