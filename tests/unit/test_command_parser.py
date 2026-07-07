import pytest
from unittest.mock import patch

# Import your functions (adjust the import path if needed)
from cli.presentation.command_parser import (
    parse_command,
    get_command,
    get_arguments,
    get_flags,
)


# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def mock_commands():
    return {
        "create": {
            "args": ["name"],
            "flags": [
                {"flag": ["-f", "--format"], "name": "format"},
                {"flag": ["-t", "--type"], "name": "type"},
            ],
        }
    }


# -------------------------
# get_command tests
# -------------------------

@pytest.mark.unit
def test_get_command_valid():
    result = get_command(["create"], ["create", "delete"])
    assert result == "create"


@pytest.mark.unit
def test_get_command_no_command():
    with pytest.raises(Exception) as exc:
        get_command([], ["create"])

    assert "NO_COMMAND" in str(exc.value)


@pytest.mark.unit
def test_get_command_unknown():
    with pytest.raises(Exception) as exc:
        get_command(["invalid"], ["create"])

    assert "UNKNOWN_COMMAND" in str(exc.value)


# -------------------------
# get_arguments tests
# -------------------------

@pytest.mark.unit
def test_get_arguments_valid():
    command = ["file.txt"]
    args = ["name"]

    result = get_arguments(command, args)

    assert result == {"name": "file.txt"}


@pytest.mark.unit
def test_get_arguments_missing():
    with pytest.raises(Exception) as exc:
        get_arguments([], ["name"])

    assert "MISSING_ARGS" in str(exc.value)


# -------------------------
# get_flags tests
# -------------------------

@pytest.mark.unit
def test_get_flags_valid():
    command = ["-f", "json", "--type", "text"]
    flags = [
        {"flag": ["-f", "--format"], "name": "format"},
        {"flag": ["-t", "--type"], "name": "type"},
    ]

    result = get_flags(command, flags)

    assert result == {"format": "json", "type": "text"}


@pytest.mark.unit
def test_get_flags_unknown_flag():
    command = ["-x", "json"]
    flags = [
        {"flag": ["-f", "--format"], "name": "format"},
    ]

    with pytest.raises(Exception) as exc:
        get_flags(command, flags)

    assert "UNKNOWN_FLAG" in str(exc.value)


@pytest.mark.unit
def test_get_flags_repeated_flag():
    command = ["-f", "json", "--format", "xml"]
    flags = [
        {"flag": ["-f", "--format"], "name": "format"},
    ]

    with pytest.raises(Exception) as exc:
        get_flags(command, flags)

    assert "REPEATED_FLAG" in str(exc.value)


@pytest.mark.unit
def test_get_flags_missing_value(capfd):
    command = ["-f"]
    flags = [
        {"flag": ["-f", "--format"], "name": "format"},
    ]

    result = get_flags(command, flags)

    # It prints error instead of raising
    out, _ = capfd.readouterr()
    assert "FLAG_WITHOUT_VALUE" in out
    assert result == {}


# -------------------------
# parse_command tests
# -------------------------

@pytest.mark.unit
@patch("cli.presentation.command_parser.get_commands")
def test_parse_command_valid(mock_get_commands, mock_commands):
    mock_get_commands.return_value = mock_commands

    command = ["app.py", "create", "file.txt", "-f", "json"]

    result = parse_command(command.copy())

    assert result[0] == "create"
    assert result[1] == {"name": "file.txt", "format": "json"}


@pytest.mark.unit
@patch("cli.presentation.command_parser.get_commands")
def test_parse_command_missing_args(mock_get_commands, mock_commands, capfd):
    mock_get_commands.return_value = mock_commands

    command = ["app.py", "create"]

    result = parse_command(command.copy())

    out, _ = capfd.readouterr()
    assert "MISSING_ARGS" in out
    assert result is None


@pytest.mark.unit
@patch("cli.presentation.command_parser.get_commands")
def test_parse_command_unknown_flag(mock_get_commands, mock_commands, capfd):
    mock_get_commands.return_value = mock_commands

    command = ["app.py", "create", "file.txt", "-x", "json"]

    result = parse_command(command.copy())

    out, _ = capfd.readouterr()
    assert "UNKNOWN_FLAG" in out
    assert result is None
