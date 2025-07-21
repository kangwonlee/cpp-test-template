# begin tests/pathman.py

import os
import pathlib


def get_file_path() -> pathlib.Path:
    """
    Get the path to the current file.
    """

    p = pathlib.Path(__file__).resolve()

    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File {p} does not exist or is not a file.")

    return p


def get_test_folder(file_path:pathlib.Path=get_file_path()) -> pathlib.Path:
    """
    Get the path to the test folder.
    """
    p = file_path.parent.resolve()

    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Test folder {p} does not exist or is not a directory.")

    return p


def get_src_folder(test_folder:pathlib.Path=get_test_folder()) -> pathlib.Path:
    p = pathlib.Path(
        os.getenv(
            'STUDENT_SRC_FOLDER',
            test_folder.parent.resolve()
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


def get_c_filename() -> str:
    """
    Get the C filename from environment variable or default to 'main.c'.
    """
    return os.getenv('C_FILENAME', 'main.c')


def get_src_file_path(
    src_folder:pathlib.Path=get_src_folder(),
    c_filename:str=get_c_filename(),
) -> pathlib.Path:
    """
    Get the path to the source file.
    """
    p = src_folder / c_filename

    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"Source file {p} does not exist or is not a file.")
    return p


def get_proj_folder(test_folder:pathlib.Path=get_test_folder()) -> pathlib.Path:
    """
    Get the project folder path.
    """
    p = pathlib.Path(
        os.getenv(
            'GITHUB_WORKSPACE',
            test_folder.parent.resolve()
        )
    )

    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Project folder {p} does not exist or is not a directory.")

    return p


# end tests/pathman.py
