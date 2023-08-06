#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `caesar_deco` package."""

import pytest

from click.testing import CliRunner

from caesar_deco import caesar_deco
from caesar_deco import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert 'Usage: main [OPTIONS] TEXTO\n\nError: Missing argument "texto".\n' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_caesar_decoder(capsys):
    assert caesar_deco.caesar_decoder("fdhvdu frgh") == None
    captured = capsys.readouterr()
    assert "['fdhvdu frgh ' 'geiwev gshi ' 'hfjxfw htij ' 'igkygx iujk '" in captured.out