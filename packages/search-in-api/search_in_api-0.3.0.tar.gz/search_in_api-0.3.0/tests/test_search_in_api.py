#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `search_in_api` package."""

import pytest

from search_in_api import search_in_api


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
