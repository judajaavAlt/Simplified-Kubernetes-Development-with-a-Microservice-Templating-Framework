from cli.userInterface.command_line_interface import(
    get_args,
    output_message,
    output_error
)
import pytest
import sys


def test_get_args(monkeypatch):
    test_args = ["program_name", "file.txt", "--verbose"]

    monkeypatch.setattr(sys, "argv", test_args)

    args = get_args()

    # Adapt this depending on how get_args returns values
    assert not (False in [arg in test_args for arg in args])


def test_output_message(capsys):
    message = "Hello world"

    output_message(message)

    captured = capsys.readouterr()

    assert captured.out.strip() == message


def test_output_error_raises_filenotfound():
    exc_type = FileNotFoundError
    message = "the file x couldn't be found in y folder"

    with pytest.raises(FileNotFoundError) as exc_info:
        output_error(exc_type, message)

    assert str(exc_info.value) == message