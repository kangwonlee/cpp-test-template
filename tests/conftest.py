# begin tests/conftest.py
import pathlib

import pytest


import pathman


@pytest.fixture(scope="module")
def file_path() -> pathlib.Path:
    p = pathlib.Path(__file__)

    assert p.exists()
    assert p.is_file()
    return p


@pytest.fixture(scope="module")
def my_test_folder(file_path:pathlib.Path) -> pathlib.Path:
    return pathman.get_test_folder(file_path)


@pytest.fixture(scope="module")
def my_src_folder(my_test_folder:pathlib.Path) -> pathlib.Path:
    return pathman.get_src_folder(my_test_folder)


@pytest.fixture(scope="module")
def c_filename():
    return pathman.get_c_filename()


@pytest.fixture(scope="module")
def src_file_path(my_src_folder:pathlib.Path, c_filename:str) -> pathlib.Path:
    """
    Fixture to provide the path to the source file.
    """
    return pathman.get_src_file_path(my_src_folder, c_filename)


@pytest.fixture(scope="module")
def obj_file_path(src_file_path:pathlib.Path, tmp_path_factory:pytest.TempPathFactory) -> pathlib.Path:
    """Fixture for the path to the object file."""
    tmp_path = tmp_path_factory.mktemp("obj_files", numbered=True)
    return (tmp_path / src_file_path.name).with_suffix(".o")


@pytest.fixture(scope="module")
def proj_folder(my_test_folder:pathlib.Path) -> pathlib.Path:
    return pathman.get_proj_folder(my_test_folder)

# end tests/conftest.py
