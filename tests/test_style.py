# begin tests/test_style.py
import difflib
import logging
import os
import pathlib
import subprocess

from typing import List


import clang.cindex
import pytest


import pathman


logging.basicConfig(level=logging.INFO)


def find_libclang() -> pathlib.Path:
    s = sorted(pathlib.Path('/usr').glob('**/libclang*.so'))
    if not s:
        pytest.fail(
            "libclang not found under `/usr`.\n"
            "Install libclang-dev or equivalent package."
        )
        result = None
    else:
        result = s[-1]
    return result


clang.cindex.Config.set_library_file(str(find_libclang()))


def get_clang_format_diff(src_file_path:pathlib.Path) -> str:
    """
    Generate a diff between the original and clang-format-corrected code, highlighting whitespace.
    """

    with open(src_file_path, 'r') as f:
        original_lines = f.readlines()

    # Run clang-format to get the formatted version
    result = subprocess.run(
        ["clang-format", str(src_file_path)],
        capture_output=True,
        text=True,
    )
    formatted_lines = result.stdout.splitlines(keepends=True)

    # Convert lines to show whitespace explicitly (e.g., ' ' -> '·', '\t' -> '→')
    def show_whitespace(lines):
        return [line.rstrip('\n').replace(' ', '·').replace('\t', '→') + '\n' for line in lines]

    # Generate a unified diff with visible whitespace
    diff = difflib.unified_diff(
        show_whitespace(original_lines),
        show_whitespace(formatted_lines),
        fromfile=str(src_file_path),
        tofile=str(src_file_path) + '.formatted',
        lineterm='',
    )
    return ''.join(diff)


def test_clang_format(src_file_path:pathlib.Path):
    """
    Test the C code for clang-format compliance and provide diff-based feedback.
    """

    # Verify the source file exists
    if not src_file_path.exists():
        pytest.fail(f"Source file not found: {src_file_path}")

    # Run clang-format to check for violations
    result = subprocess.run(
        [
            "clang-format",
            "--dry-run", "--Werror", "--verbose",
            str(src_file_path),
        ],
        capture_output=True,
        text=True,
    )

    # If clang-format fails, provide diff-based feedback
    if result.returncode != 0:
        # Generate diff to show corrections
        diff = get_clang_format_diff(src_file_path)

        # Construct relative path for student instructions
        relative_path = src_file_path.relative_to(os.getenv('GITHUB_WORKSPACE', '.'))

        feedback = (
            "clang-format detected formatting issues in your code.\n"
            "Suggested changes (diff, · = space, → = tab):\n"
            f"{diff if diff else 'No diff available (ensure clang-format is installed).'}\n\n"
            f"To fix, run: clang-format -i {relative_path}\n"
            "Ensure your .clang-format file matches the assignment's style (e.g., Google).\n"
            "Check the diff for changes (spaces shown as ·, tabs as →)."
        )

        assert result.returncode == 0, feedback


class CKeywordChecker:
    def __init__(self, func_name):
        self.func_name = func_name
        self.has_if = False
        self.disallowed = []  # List of (construct, line) tuples

    def check(self, cursor):
        logging.info(f"Starting to check function: {self.func_name}")
        for c in cursor.get_children():  # Traverse top-level declarations
            if c.kind == clang.cindex.CursorKind.FUNCTION_DECL and c.spelling == self.func_name:
                logging.info(f"Found function: {self.func_name}")
                for child in c.walk_preorder():
                    logging.info(f"child.spelling: {child.spelling}")
                    logging.info(f"child.kind: {child.kind}")
                    if child.kind == clang.cindex.CursorKind.IF_STMT:
                        logging.info(f"found if statement in {self.func_name} at line {child.location.line}")
                        self.has_if = True
                    elif child.kind == clang.cindex.CursorKind.FOR_STMT:
                        logging.info(f"found for statement in {self.func_name} at line {child.location.line}")
                        self.disallowed.append(('for', child.location.line))
                    elif child.kind == clang.cindex.CursorKind.WHILE_STMT:
                        logging.info(f"found while statement in {self.func_name} at line {child.location.line}")
                        self.disallowed.append(('while', child.location.line))
                    elif child.kind == clang.cindex.CursorKind.CONDITIONAL_OPERATOR:
                        logging.info(f"found conditional operator statement in {self.func_name} at line {child.location.line}")
                        self.disallowed.append(('ternary operator (?:)', child.location.line))

        logging.info(f"Finished checking function: {self.func_name}")


def test_src_file_exists(src_file_path:pathlib.Path):
    """
    Test that the source file exists.
    """
    if not src_file_path.exists():
        pytest.fail(f"Source file not found: {src_file_path}")


def get_TranslationUnit(src_file_path:pathlib.Path) -> clang.cindex.TranslationUnit:
    """
    Parse the source file using libclang and return the translation unit.
    """
    index = clang.cindex.Index.create()
    tu = index.parse(str(src_file_path), args=['-std=c99'])

    # Check for parse errors
    errors = [d for d in tu.diagnostics if d.severity >= clang.cindex.Diagnostic.Error]
    if errors:
        error_msgs = "\n".join([f"{d.location.file}:{d.location.line}:{d.location.column}: {d.spelling}" for d in errors])
        pytest.fail(f"Parse errors in code:\n{error_msgs}. Ensure your code compiles and uses only allowed headers (stdio.h).")

    return tu


@pytest.fixture(scope="module")
def tu(src_file_path:pathlib.Path) -> clang.cindex.TranslationUnit:
    return get_TranslationUnit(src_file_path)


def function_names(
    tu:clang.cindex.TranslationUnit=get_TranslationUnit(pathman.get_src_file_path()),
) -> List[str]:
    names = []
    for c in tu.cursor.get_children():
        if c.kind == clang.cindex.CursorKind.FUNCTION_DECL and c.spelling != 'main':
            if c.location.file and c.location.file.name == tu.spelling:
                names.append(c.spelling)
    return names


@pytest.mark.parametrize("func_name", function_names())
def test_conditional_usage(
    src_file_path:pathlib.Path,
    func_name:str,
    tu:clang.cindex.TranslationUnit
):
    """
    Test that get_sign and get_water_state use if/else and do not use for, while, or ternary operators.
    """

    logging.info(f"Checking function {func_name} of source file: {src_file_path}")

    # Check each function
    checker = CKeywordChecker(func_name)
    checker.check(tu.cursor)

    # Check for required if statements
    assert checker.has_if, (
        f"Function {func_name} must use if/else statements as per assignment instructions. "
        "No if statements found."
    )

    # Check for disallowed constructs
    if checker.disallowed:
        feedback = (
            f"Function {func_name} contains disallowed constructs:\n" +
            '\n'.join([f"- {construct} at line {line}" for construct, line in checker.disallowed]) +
            "\nUse if/else statements instead of loops or ternary operators."
        )
        assert not checker.disallowed, feedback


# Run tests if invoked directly
if "__main__" == __name__:
    pytest.main(['--verbose', __file__])

# end tests/test_style.py
