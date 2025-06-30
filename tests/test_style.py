# begin tests/test_style.py
import difflib
import pathlib
import subprocess
import os

import pytest

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


# Run tests if invoked directly
if "__main__" == __name__:
    pytest.main(['--verbose', __file__])

# end tests/test_style.py
