# begin test/test_pointers.py

import re
import subprocess


import pytest


def test_c_syntax():
    # Clean and rebuild
    subprocess.run(["make", "clean"], check=True)

    cmake_result = subprocess.run(["cmake", "."], capture_output=True, text=True, check=True)
    make_result = subprocess.run(["make"], capture_output=True, text=True, check=True)

    # Check for syntax errors in the build output
    if "error:" in cmake_result.stderr:
        # Generate comments on syntax errors
        comments = generate_comments_on_c_syntax_errors(cmake_result.stderr)
        assert False, f"cmake error:\n{comments}"

    # Check for syntax errors in the build output
    if "error:" in make_result.stderr:
        # Generate comments on syntax errors
        comments = generate_comments_on_c_syntax_errors(make_result.stderr)
        assert False, f"C syntax errors found:\n{comments}"


def generate_comments_on_c_syntax_errors(build_output):
    error_pattern = r"(.*\.[ch]:\d+:\d+:\s*error:.*)"
    errors = re.findall(error_pattern, build_output)
    comments = ""
    for error in errors:
        # Split the error message into parts
        file_name, line_number, error_message = error.split(":", 2)
        # Generate a comment
        comment = f"// Error in {file_name} on line {line_number}: {error_message.strip()}"
        comments += comment + "\n"
    return comments


@pytest.mark.parametrize("test_function", [
    "test_allocate_integer_valid_pointer",
    "test_allocate_integer_correct_size",
    "test_allocate_integer_set_value",
    "test_deallocate_integer_frees_memory"
])
def test_c_functions(test_function):
    result = subprocess.run(["./my_tests", test_function], capture_output=True, text=True)

    # Check return code for pass/fail
    assert result.returncode == 0, f"Test '{test_function}' failed: {result.stderr}"

    # Optionally, check stdout/stderr for specific messages
    # assert "Expected output" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__])

# end test/test_pointers.py
