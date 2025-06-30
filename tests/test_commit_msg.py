# begin tests/test_commit_msg.py
import datetime
import functools
import pathlib
import re
import subprocess

from typing import Dict, List


Commit = Dict[str, str]
CommitLog = List[Commit]


import pytest


def commit_to_dict(line:str) -> Commit:
    dateformat = r"%Y-%m-%d %H:%M:%S %z"

    values = line.strip().split('\t')
    return {
        'sha': values[0],
        'name': values[1],
        'date': datetime.datetime.strptime(values[2], dateformat),
        'message': ('\t'.join(values[3:])).strip(),
    }


@pytest.fixture
def git_log(proj_folder:pathlib.Path) -> CommitLog:
    result = tuple(
        map(
            commit_to_dict,
            subprocess.check_output(
                ['git', 'log', '--pretty=%h%x09%an%x09%ad%x09%s', '--date=iso'],
                encoding='utf-8',
                cwd=proj_folder,
            ).splitlines()
        )
    )

    return result


@functools.lru_cache(maxsize=1)
def re_update_one_filename() -> re.Pattern:
    return re.compile(r"^(update\s*[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9]+)?)[-\s\.]*\d*[-\s\.]*?$", re.I)


def test_re_update_exercise(c_filename:str):
    """
    Test the regular expression for update_one_filename.py
    update_one_filename.py 에 대한 정규 표현식을 테스트합니다.
    """
    pattern = re_update_one_filename()

    assert pattern.search("update exercise.py")
    assert pattern.search("update exercise.py 1")
    assert pattern.search("update exercise.py 2")
    assert pattern.search("update exercise.py 22")
    assert pattern.search("update exercise.py.6")
    assert pattern.search("update exercise.py-789")

    assert pattern.search(f"update {c_filename}")
    assert pattern.search(f"update {c_filename} 1")
    assert pattern.search(f"update {c_filename} 2")
    assert pattern.search(f"update {c_filename} 22")
    assert pattern.search(f"update {c_filename}.6")
    assert pattern.search(f"update {c_filename}-789")

    assert pattern.search("update words.txt")
    assert pattern.search("update words.txt 1")
    assert pattern.search("update words.txt 2")
    assert pattern.search("update words.txt 22")
    assert pattern.search("update words.txt.6")
    assert pattern.search("update words.txt-789")


def is_commit_message_too_simple(message:str) -> bool:
    """
    Check if the commit message is too simple.
    커밋 메시지가 너무 간단한지 확인합니다.
    """
    using_default = (
        re_update_one_filename().search(message)
    )

    simple_fix = (
        re.search(r"^(fix|fixed|change|changed|edit|modified|수정|변경)\s*\d*$", message, re.I)
    )

    digits_only = (
        message.isdigit()
    )

    too_short = (
        len(message) < 10
    )

    too_few_words = (
        len(
            tuple(
                filter(
                    lambda w: len(w)>1,
                    message.split()
                )
            )
        ) < 5
    )

    return any((
        using_default,
        simple_fix,
        digits_only,
        too_short,
        too_few_words,
    ))


def test_git_log__last_message(git_log:CommitLog):
    latest_commit = git_log[0]

    assert (not is_commit_message_too_simple(latest_commit['message'])), (
        f"Please use more descriptive commit message : {latest_commit['message']}\n"
        f"커밋 메시지에 보다 자세히 설명 바랍니다 : {latest_commit['message']}\n"
        "See https://cbea.ms/git-commit/\n"
        "참고 : https://velog.io/@k-minsik/좋은-Git-Commit-message-작성법"
    )


if __name__ == "__main__":
    pytest.main([__file__])

# end tests/test_commit_msg.py
