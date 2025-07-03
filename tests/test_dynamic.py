# begin test/test_dynamic.py
import pathlib
import subprocess


import pytest


@pytest.fixture(scope="module")
def result(proj_folder:pathlib.Path, exec_name:str="my_exec") -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(proj_folder / "tests" / exec_name)],
        capture_output=True,
        text=True,
    )


def test_hello_world_output(
    result:subprocess.CompletedProcess
) -> None:
    """
    Test whether the program outputs 'Hello World' with a newline.
    """
    assert result.returncode == 0, f"Program failed with return code {result.returncode}\nstderr: {result.stderr}"
    assert result.stdout == "Hello World\n", f"Expected 'Hello World\\n', got '{result.stdout}'"


if __name__ == "__main__":
    pytest.main([__file__])

# end test/test_dynamic.py
