# begin tests/test_build.py
import pathlib
import subprocess

import pytest


def test_could_find_src_files(src_file_path: pathlib.Path):
    """
    Test the find_src_files function.
    """
    assert src_file_path.exists(), f"Source file {src_file_path} does not exist"
    assert src_file_path.is_file(), f"{src_file_path} is not a file"
    assert src_file_path.suffix == '.cpp', f"Expected a .cpp file, got {src_file_path.suffix}"


def test_build(src_file_path: pathlib.Path, obj_file_path: pathlib.Path):
    """
    Test the build command.
    """
    result = subprocess.run(
        [
            "clang++",
            "-c", str(src_file_path),
            '-o', str(obj_file_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Build failed\n"
        f"stdout : {result.stdout}\n"
        f"stderr : {result.stderr}\n"
    )


if "__main__" == __name__:
    pytest.main(['--verbose', __file__])

# end tests/test_build.py
