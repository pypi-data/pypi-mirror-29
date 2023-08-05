import configparser
import os
import shutil
import tempfile
import time
from pathlib import Path

import pytest
from giturlparse import parse

from release_exporter.exceptions import ParserError
from release_exporter.utils import get_repo_url_info, date_convert, multi_key_gitlab, description

DUP_SECTION = """\
[branch "v3"]
[travis]
    slug = akshaybabloo/gollahalli-me
[branch "v3"]
    remote = origin
    merge = refs/heads/v3
"""

PASS_SECTION = """\
[remote "origin"]
    url = git@github.com:akshaybabloo/release-exporter.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master
"""


def temp_file(value):
    temp_location = tempfile.gettempdir()
    os.chdir(temp_location)

    p = Path('.git/')

    if p.is_dir():
        shutil.rmtree(temp_location + os.sep + '.git')

    time.sleep(1)

    os.mkdir('.git/')

    with open(temp_location + os.sep + '.git' + os.sep + 'config', 'w') as config_file:
        config_file.write(value)

# ---------------------- get_repo_url_info ------------------


def test_get_repo_url_info_args():
    content = get_repo_url_info(
        repo_url='https://github.com/akshaybabloo/release-exporter.git')

    assert parse(
        'https://github.com/akshaybabloo/release-exporter.git').owner == content.owner


def test_get_repo_url_info_fail():
    with pytest.raises(ParserError,
                       message='Git config file does not exist please provide the repository url by using --url.'):
        content = get_repo_url_info(location='yo')


def test_get_repo_url_info_pass():
    t = tempfile.gettempdir()
    temp_file(PASS_SECTION)

    content = get_repo_url_info(location=t)

    assert content.owner == 'akshaybabloo'


def test_get_repo_url_info_fail_2():
    t = tempfile.gettempdir()
    temp_file(DUP_SECTION)

    with pytest.raises(configparser.DuplicateSectionError,
                       message='There seems to be a duplicate section in your config. Try giving the repository URL by using --url.'):
        content = get_repo_url_info(location=t)


# ---------------- date_convert -----------------------


def test_date_convert_fail():
    with pytest.raises(ValueError, message="Unknown string format"):
        content = date_convert('10-10-2019T12:12:12z')


def test_date_convert_pass():
    content = date_convert('10-10-2019')
    assert content == '2019-10-10'


def test_date_convert_pass2():
    content = date_convert('2008-01-14T04:33:35Z')
    assert content == '2008-01-14'


# ----------------- multi_key_gitlab ------------------


def test_multi_key_gitlab_pass():
    data = {
        "owner": {
            "username": "user"
        }
    }

    content = multi_key_gitlab(data)
    assert content == "user"


def test_multi_key_gitlab_pass_except():
    data = {
        "owner": "user"
    }

    content = multi_key_gitlab(data)
    assert content == None


# ------------- description ------------

def test_description_pass():
    provider = "some provider"
    repo_name = "some repo name"
    tags_number = 22

    expected = '\n'.join(['+-----------------+----------------+',
                          '| Provider        | some provider  |',
                          '+-----------------+----------------+',
                          '| Repository Name | some repo name |',
                          '+-----------------+----------------+',
                          '| Number of Tags  | 22             |',
                          '+-----------------+----------------+'])

    actual = description(provider, repo_name, tags_number)

    assert actual == expected


def test_description_fail():
    provider = "some provider"
    repo_name = "some repo name"

    expected = '\n'.join(['+-----------------+----------------+',
                          '| Provider        | some provider  |',
                          '+-----------------+----------------+',
                          '| Repository Name | some repo name |',
                          '+-----------------+----------------+',
                          '| Number of Tags  | 22             |',
                          '+-----------------+----------------+'])

    actual = description(provider, repo_name)

    assert actual != expected
