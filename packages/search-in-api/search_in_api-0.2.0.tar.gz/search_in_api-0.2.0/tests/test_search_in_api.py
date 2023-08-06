#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `search_in_api` package."""

import pytest

from click.testing import CliRunner

from search_in_api import search_in_api
from search_in_api import cli


@pytest.fixture
def params():
    """
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return {
        "url": "https://raw.githubusercontent.com/archatas/search_in_api/master/tests/data/sample-data.xml",
        "tag": "artist",
        "value": "Joachim Pastor",
    }


def test_search_in_string(params):
    """Test the core function"""
    pages = search_in_api.search_for_string(
        url=params['url'],
        tag=params['tag'],
        value=params['value'],
    )
    assert pages == [
        "https://raw.githubusercontent.com/archatas/search_in_api/master/tests/data/sample-data.xml",
        "https://raw.githubusercontent.com/archatas/search_in_api/master/tests/data/sample-data3.xml",
    ]


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'search_in_api.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
