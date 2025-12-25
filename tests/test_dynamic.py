# begin tests/test_dynamic.py
import pathlib
import re
import subprocess

from typing import Dict

import pytest


def extract_variables(source_path: pathlib.Path) -> Dict[str, float]:
    """Extract values of a, b, c, d from main.c. Looks for simple variable declarations."""
    with source_path.open("r") as f:
        code = f.read()
    patterns = {
        "a": r"int\s+a\s*=\s*([+-]?\d+)\s*;",
        "b": r"int\s+b\s*=\s*([+-]?\d+)\s*;",
        "c": r"float\s+c\s*=\s*([+-]?(?:\d+\.?\d*|\d*\.\d+)(?:[eE][+-]?\d+)?)[fFlL]?\s*;",
        "d": r"float\s+d\s*=\s*([+-]?(?:\d+\.?\d*|\d*\.\d+)(?:[eE][+-]?\d+)?)[fFlL]?\s*;"
    }
    variables = {}
    for var, pattern in patterns.items():
        match = re.search(pattern, code)
        if not match:
            pytest.fail(f"Missing declaration for '{var}' in main.c. Example: 'int a = 5;' or 'float c = 0.1;'")
        variables[var] = float(match.group(1))
    return variables


def compute_expected_output(variables: Dict[str, float], line_index: int) -> str:
    """Generate expected output for a specific line (0-12)."""
    a, b, c, d = variables["a"], variables["b"], variables["c"], variables["d"]
    lines = [
        f"a = {int(a)}\n",  # Line 0
        f"b = {int(b)}\n",  # Line 1
        f"a + b = {int(a + b)}\n",  # Line 2
        f"a - b = {int(a - b)}\n",  # Line 3
        f"a * b = {int(a * b)}\n",  # Line 4
        f"a / b = {int(a / b)}\n",  # Line 5
        "==========\n",  # Line 6
        f"c = {c:.8f}\n",  # Line 7
        f"d = {d:.8f}\n",  # Line 8
        f"c + d = {(c + d):.8f}\n",  # Line 9
        f"c - d = {(c - d):.8f}\n",  # Line 10
        f"c * d = {(c * d):.8f}\n",  # Line 11
        f"c / d = {(c / d):.8f}\n"   # Line 12
    ]
    return lines[line_index]


@pytest.fixture(scope="module")
def result(my_test_folder: pathlib.Path) -> subprocess.CompletedProcess:
    """Run the C program executable (my_exec) and capture its output."""
    exec_name = "my_exec"
    try:
        return subprocess.run(
            [str(my_test_folder / exec_name)],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Program execution timed out")
    except FileNotFoundError:
        pytest.fail(f"Executable not found: {my_test_folder / exec_name}")


@pytest.fixture(scope="module")
def result_stdout(result: subprocess.CompletedProcess) -> str:
    return result.stdout


@pytest.fixture(scope="module")
def sep() -> str:
    return "=" * 10 + "\n"


@pytest.fixture(scope="module")
def expected_num_sep() -> int:
    return 1


def test_number_of_separators(result_stdout:str, sep:str, expected_num_sep:int) -> str:
    count = result_stdout.splitlines().count(sep.strip())

    if count != expected_num_sep:
        pytest.fail(f'expected number of separators == {expected_num_sep} but got {count}')


@pytest.fixture(scope="module")
def variables(src_file_path: pathlib.Path) -> Dict[str, float]:
    """Extract variables a, b, c, d from main.c."""
    return extract_variables(src_file_path)


def test_no_division_by_zero(variables: Dict[str, float]):
    """Check that b and d are not zero to avoid division by zero."""
    assert variables["b"] != 0, "Variable 'b' cannot be 0 (division by zero). Set b to a non-zero value, e.g., 'int b = 5;'."
    assert variables["d"] != 0, "Variable 'd' cannot be 0 (division by zero). Set d to a non-zero value, e.g., 'float d = 0.2;'."


@pytest.mark.parametrize(
    "line_index, description, printf_format",
    [
        (0, "a = [value]", "printf('a = %d\\n', a)"),
        (1, "b = [value]", "printf('b = %d\\n', b)"),
        (2, "a + b = [result]", "printf('a + b = %d\\n', a + b)"),
        (3, "a - b = [result]", "printf('a - b = %d\\n', a - b)"),
        (4, "a * b = [result]", "printf('a * b = %d\\n', a * b)"),
        (5, "a / b = [result]", "printf('a / b = %d\\n', a / b)")
    ],
    ids=["print_a", "print_b", "integer_addition", "integer_subtraction", "integer_multiplication", "integer_division"]
)
def test_integer_operations(result: subprocess.CompletedProcess, variables: Dict[str, float], line_index: int, description: str, printf_format: str):
    """Check if integer operation outputs print correctly."""
    assert result.returncode == 0, "Program crashed. Check main.c for errors."
    output_lines = result.stdout.splitlines(keepends=True)
    assert len(output_lines) >= line_index + 1, f"Missing output for '{description}'. Add {printf_format}."
    expected = compute_expected_output(variables, line_index)
    assert output_lines[line_index] == expected, f"Line {line_index + 1}: expected '{expected.strip()}', got '{output_lines[line_index].strip()}'. Use {printf_format}."


@pytest.mark.parametrize(
    "line_index, description, printf_format",
    [
        ( 7, "c = [value]", "printf('c = %.8f\\n', c)"),
        ( 8, "d = [value]", "printf('d = %.8f\\n', d)"),
        ( 9, "c + d = [result]", "printf('c + d = %.8f\\n', c + d)"),
        (10, "c - d = [result]", "printf('c - d = %.8f\\n', c - d)"),
        (11, "c * d = [result]", "printf('c * d = %.8f\\n', c * d)"),
        (12, "c / d = [result]", "printf('c / d = %.8f\\n', c / d)")
    ],
    ids=["print_c", "print_d", "float_addition", "float_subtraction", "float_multiplication", "float_division"]
)
def test_float_values(result: subprocess.CompletedProcess, variables: Dict[str, float], line_index: int, description: str, printf_format: str):
    """Check if float operation outputs have correct values."""
    assert result.returncode == 0, "Program crashed. Check main.c for errors."
    output_lines = result.stdout.splitlines(keepends=True)
    assert len(output_lines) >= line_index + 1, f"Missing output for '{description}'. Add {printf_format}."
    expected = compute_expected_output(variables, line_index)
    got_value = float(output_lines[line_index].split("=")[1].strip())
    expected_value = float(expected.split("=")[1].strip())
    assert abs(got_value - expected_value) < 1e-5, f"Line {line_index + 1}: expected '{expected.strip()}', got '{output_lines[line_index].strip()}'. Use {printf_format}."


@pytest.mark.parametrize(
    "line_index, regex_pattern, description, printf_format",
    [
        ( 7, r"c\s*=\s*[-]?\d*\.\d{8}\n", "c = [value]", "printf('c = %.8f\\n', c)"),
        ( 8, r"d\s*=\s*[-]?\d*\.\d{8}\n", "d = [value]", "printf('d = %.8f\\n', d)"),
        ( 9, r"c\s*\+\s*d\s*=\s*[-]?\d*\.\d{8}\n", "c + d = [result]", "printf('c + d = %.8f\\n', c, d, c + d)"),
        (10, r"c\s*-\s*d\s*=\s*[-]?\d*\.\d{8}\n", "c - d = [result]", "printf('c - d = %.8f\\n', c, d, c - d)"),
        (11, r"c\s*\*\s*d\s*=\s*[-]?\d*\.\d{8}\n", "c * d = [result]", "printf('c * d = %.8f\\n', c, d, c * d)"),
        (12, r"c\s*/\s*d\s*=\s*[-]?\d*\.\d{8}\n", "c / d = [result]", "printf('c / d = %.8f\\n', c, d, c / d)")
    ],
    ids=["c_decimal_digits", "d_decimal_digits", "float_addition_decimal_digits", "float_subtraction_decimal_digits", "float_multiplication_decimal_digits", "float_division_decimal_digits"]
)
def test_float_decimal_digits(result: subprocess.CompletedProcess, line_index: int, regex_pattern: str, description: str, printf_format: str):
    """Check if float outputs have 8 decimal places."""
    assert result.returncode == 0, "Program crashed. Check main.c for errors."
    output_lines = result.stdout.splitlines(keepends=True)
    assert len(output_lines) >= line_index + 1, f"Missing output for '{description}'. Add {printf_format}."
    if not re.match(regex_pattern, output_lines[line_index]):
        raise AssertionError(
            f"Line {line_index + 1}: expected '{description}' with 8 decimal places, got '{output_lines[line_index].strip()}'. Use {printf_format}."
        )


if __name__ == "__main__":
    """Entry point for running tests directly."""
    pytest.main(['-vv', __file__])

# end tests/test_dynamic.py
