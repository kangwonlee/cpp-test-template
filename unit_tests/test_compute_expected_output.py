# begin unit_tests/test_compute_expected_output.py

import pytest


class TestComputeExpectedOutput:
    """Test expected output computation for different line indices."""

    @pytest.fixture
    def sample_variables(self):
        return {"a": 10.0, "b": 3.0, "c": 0.5, "d": 0.2}

    def test_line_0_integer_a(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 0)
        assert expected == "a = 10\n"

    def test_line_1_integer_b(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 1)
        assert expected == "b = 3\n"

    def test_line_2_addition(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 2)
        assert expected == "a + b = 13\n"

    def test_line_3_subtraction(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 3)
        assert expected == "a - b = 7\n"

    def test_line_4_multiplication(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 4)
        assert expected == "a * b = 30\n"

    def test_line_5_division(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 5)
        assert expected == "a / b = 3\n"

    def test_line_6_separator(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 6)
        assert expected == "==========\n"

    def test_line_7_float_c(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 7)
        assert expected == "c = 0.50000000\n"

    def test_line_8_float_d(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 8)
        assert expected.startswith("d = 0.2")
        assert len(expected.split("=")[1].strip().split(".")[1]) == 8

    def test_line_9_float_addition(self, compute_expected_output, sample_variables):
        expected = compute_expected_output(sample_variables, 9)
        assert expected.startswith("c + d = 0.7")

    def test_negative_values(self, compute_expected_output):
        vars_with_negatives = {"a": -5.0, "b": 2.0, "c": -0.1, "d": 0.3}
        expected = compute_expected_output(vars_with_negatives, 3)
        assert expected == "a - b = -7\n"

# end unit_tests/test_compute_expected_output.py
