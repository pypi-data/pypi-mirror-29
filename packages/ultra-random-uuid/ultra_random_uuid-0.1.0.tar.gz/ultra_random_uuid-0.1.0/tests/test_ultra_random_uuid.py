#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ultra_random_uuid` package."""


import unittest
from click.testing import CliRunner

from ultra_random_uuid import ultra_random_uuid
from ultra_random_uuid import cli


class TestUltra_random_uuid(unittest.TestCase):
    """Tests for `ultra_random_uuid` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'ultra_random_uuid.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
