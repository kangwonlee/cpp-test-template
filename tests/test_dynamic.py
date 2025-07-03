# begin test/test_dynamic.py
import pathlib
import subprocess


import pytest


@pytest.fixture(scope="module")
def result(my_test_folder:pathlib.Path, exec_name:str="my_exec") -> subprocess.CompletedProcess:
    try:
        r = subprocess.run(
            [str(my_test_folder / exec_name)],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired as e:
        pytest.fail(f"Execution timed out: {e}")

    return r


def test_expected_output(
    result:subprocess.CompletedProcess,
    expected_stdout:str="Hello World\n",
) -> None:
    """
    Test whether the program outputs the expected string.
    """
    assert result.returncode == 0, f"Program failed with return code {result.returncode}\nstderr: {result.stderr}"
    assert result.stdout == expected_stdout, f"Expected {expected_stdout!r}, got '{result.stdout!r}'"


if __name__ == "__main__":
    pytest.main([__file__])

# end test/test_dynamic.py
