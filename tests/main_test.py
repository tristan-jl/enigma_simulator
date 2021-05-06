import argparse
from unittest import mock

import pytest

from enigma_simulator import main


def test_help_command():
    with pytest.raises(SystemExit):
        main.main(["--help"])


@pytest.fixture
def argparse_parse_args_spy():
    parse_args_mock = mock.Mock()

    original_parse_args = argparse.ArgumentParser.parse_args

    def fake_parse_args(self, args):
        parse_args_mock(args)
        return original_parse_args(self, args)

    with mock.patch.object(
        argparse.ArgumentParser,
        "parse_args",
        fake_parse_args,
    ):
        yield parse_args_mock


def test_enigma_settings(argparse_parse_args_spy):
    args = [
        "-n",
        "I",
        "II",
        "III",
        "-s",
        "1",
        "2",
        "3",
        "-r",
        "B",
        "-c",
        "AB HF",
        "AAA",
        "hello",
    ]

    main.main(args)
    argparse_parse_args_spy.assert_has_calls([mock.call(args)])
