# begin unit_tests/conftest.py

import pathlib
import sys


import pytest


# Add tests directory to path for importing test_dynamic
unit_test_path = pathlib.Path(__file__).parent.resolve()
project_root = unit_test_path.parent.resolve()
tests_path = project_root / "tests"
sys.path.insert(0, str(tests_path))

import test_dynamic


@pytest.fixture
def extract_variables():
    """Provide extract_variables function for testing."""
    return test_dynamic.extract_variables


@pytest.fixture
def compute_expected_output():
    """Provide compute_expected_output function for testing."""
    return test_dynamic.compute_expected_output


@pytest.fixture
def fixtures_dir():
    """Path to fixtures directory."""
    return pathlib.Path(__file__).parent / "fixtures"

# end unit_tests/conftest.py
