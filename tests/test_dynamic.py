# begin test/test_dynamic.py
import pathlib
import subprocess


import pytest


def test_hello_world_output(proj_folder: pathlib.Path):
    """Test that the program outputs 'Hello World' with a newline."""
    result = subprocess.run(
        [str(proj_folder / "build" / "hello")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Program failed with return code {result.returncode}\nstderr: {result.stderr}"
    assert result.stdout == "Hello World\n", f"Expected 'Hello World\\n', got '{result.stdout}'"


if __name__ == "__main__":
    pytest.main([__file__])

# end test/test_dynamic.py
