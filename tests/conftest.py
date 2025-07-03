# begin tests/conftest.py

import os
import pathlib


import pytest


@pytest.fixture(scope="module")
def file_path() -> pathlib.Path:
    p = pathlib.Path(__file__)
    assert p.exists()
    assert p.is_file()
    return p


@pytest.fixture(scope="module")
def my_test_folder(file_path:pathlib.Path) -> pathlib.Path:
    p = file_path.parent.resolve()
    assert p.exists()
    assert p.is_dir()
    return p


@pytest.fixture(scope="module")
def my_src_folder(my_test_folder:pathlib.Path) -> pathlib.Path:
    p = pathlib.Path(
        os.getenv(
            'STUDENT_SRC_FOLDER',
            my_test_folder.parent.resolve()
        )
    )
    assert p.exists()
    assert p.is_dir()

    # Ensure the folder contains C source files
    if not tuple(p.glob('**/*.c')):
        raise FileNotFoundError(
            f"No C source files found in {p}\n"
            f"p.glob('*') starts with : {list(p.glob('*'))[:5]}\n"
        )

    return p


@pytest.fixture(scope="module")
def c_filename():
    return os.getenv(
        'C_FILENAME',
        'main.c',
    )


@pytest.fixture(scope="module")
def src_file_path(my_src_folder:pathlib.Path, c_filename:str) -> pathlib.Path:
    """
    Fixture to provide the path to the source file.
    """
    return my_src_folder / c_filename


@pytest.fixture(scope="module")
def obj_file_path(src_file_path:pathlib.Path, tmp_path_factory:pytest.TempPathFactory) -> pathlib.Path:
    """Fixture for the path to the object file."""
    tmp_path = tmp_path_factory.mktemp("obj_files", numbered=True)
    return (tmp_path / src_file_path.name).with_suffix(".o")


@pytest.fixture(scope="module")
def proj_folder(my_test_folder:pathlib.Path) -> pathlib.Path:
    p = pathlib.Path(
        os.getenv(
            'GITHUB_WORKSPACE',
            my_test_folder.parent.resolve()
        )
    )
    assert p.exists()
    assert p.is_dir()
    return p

# end tests/conftest.py
