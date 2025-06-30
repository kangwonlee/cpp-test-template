# begin test/test_dynamic.py
import subprocess

import pytest

@pytest.mark.parametrize("test_function", [
    "test_allocate_integer_valid_pointer",
    "test_allocate_integer_correct_size",
    "test_allocate_integer_set_value",
    "test_deallocate_integer_frees_memory"
])
def test_c_functions(test_function):

    result = subprocess.run(
        ["./my_tests", test_function],
        capture_output=True,
        text=True,
        timeout=5,
    )

    # Check return code for pass/fail
    assert result.returncode == 0, f"Test '{test_function}' failed: {result.stderr}"

    # Optionally, check stdout/stderr for specific messages
    # assert "Expected output" in result.stdout


def test_memory_leak_valgrind():
    '''
    Run the program with Valgrind to check for memory leaks
    '''

    result = subprocess.run(
        ["valgrind", "--leak-check=full", "./my_tests"],
        capture_output=True,
        text=True,
    )

    # Check if Valgrind found any memory leaks
    if "definitely lost: 0 bytes in 0 blocks" not in result.stdout:
        pytest.fail(f"Memory leak detected:\n{result.stdout}")

    # Optionally, check for other Valgrind errors
    if "ERROR SUMMARY: 0 errors from 0 contexts" not in result.stdout:
        pytest.fail(f"Valgrind reported errors:\n{result.stdout}")


if __name__ == "__main__":
    pytest.main([__file__])

# end test/test_dynamic.py
