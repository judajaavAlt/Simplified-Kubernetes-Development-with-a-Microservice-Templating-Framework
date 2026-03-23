from cli.userInterface.command_line_interface import(
    get_args,
    output_message,
)
import pytest
import sys


@pytest.mark.unit
def test_get_args(monkeypatch):
    test_args = ["program_name", "file.txt", "--verbose"]

    monkeypatch.setattr(sys, "argv", test_args)

    args = get_args()

    # Adapt this depending on how get_args returns values
    assert not (False in [arg in test_args for arg in args])


@pytest.mark.unit
def test_output_message(capsys):
    message = "Hello world"

    output_message(message)

    captured = capsys.readouterr()

    assert captured.out.strip() == message
