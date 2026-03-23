"""
Command Parser Module

This module is responsible for parsing CLI commands from plain text input.
It transforms a raw list of strings (typically sys.argv) into a structured
representation containing the command name, its positional arguments, and
associated flags.

The parsing process includes:
- Loading command definitions from a JSON configuration file
- Validating the command name against known commands
- Extracting positional arguments in the defined order
- Parsing flags (short and long forms) and mapping them to their canonical names
- Validating input (missing arguments, unknown commands, invalid or repeated flags)

The output is a structured representation that can be used by the
application to execute the requested command.

Expected command format:
    <app> <command> <arg1> <arg2> ... <flag1> <value1> ...

Example:
    app.py create file.txt -f json

Returns:
    A list containing:
        - command name (str)
        - dictionary with parsed arguments and flags (dict[str, str])

Raises:
    Exception: If the command is invalid, incomplete, or contains unknown/repeated flags.
"""

import json
from cli.constants.status import (
    ParseError
)
from pathlib import Path


def get_commands() -> dict:
    """
    Load available command definitions from the configuration file.

    Reads the `commands.JSON` file located in the same directory as this
    module and returns its contents as a dictionary.

    Returns:
        dict: A dictionary where keys are command names and values contain
            their argument and flag definitions.

    Raises:
        FileNotFoundError: If the `commands.JSON` file does not exist.
        json.JSONDecodeError: If the file contents are not valid JSON.
    """
    path = Path(__file__).parent / "commands.JSON"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_command(command: list[str]) -> dict[str, str]:
    """
    Parse a raw command input into a structured representation.

    Processes a list of strings (e.g., sys.argv), extracts the command name,
    positional arguments, and flags, returning them in a structured format.
    Removes the application name from the input, validates the command,
    extracts arguments, and parses flags.

    Args:
        command (list[str]): Raw command input.

    Returns:
        list: A list containing:
            - command name (str)
            - dictionary with parsed arguments and flags (dict[str, str])

    Raises:
        Exception: If parsing fails due to invalid command, missing arguments,
            or unknown/repeated flags.
    """
    # Remove application name
    command.pop(0)
    commands_list = get_commands()
    command_names = list(commands_list.keys())

    try:
        command_name = get_command(command, command_names)
        command.pop(0)

        command_data = commands_list[command_name]
        args = command_data["args"]
        flags = command_data["flags"]

        command_args = get_arguments(command, args)
        command = command[len(args):]

        command_flags = get_flags(command, flags)

        return [command_name, command_args | command_flags]
    except Exception as error:
        print(str(error))


def get_command(command: list[str],
                command_names: list[str]) -> str:
    """
    Validate and extract the command name from input.

    Checks that the command input is not empty and that the first element
    matches a known command name.

    Args:
        command (list[str]): Command input without the application name.
        command_names (list[str]): List of valid command names.

    Returns:
        str: The validated command name.

    Raises:
        Exception: If no command is provided or if the command is unknown.
    """
    if len(command) == 0:
        raise Exception(f"[Error {ParseError.NO_COMMAND}] "
                        "NO_COMMAND: No command was defined")

    if command[0] not in command_names:
        raise Exception(f"[Error {ParseError.UNKNOWN_COMMAND}] "
                        "UNKNOWN_COMMAND: "
                        f"{command[0]} is not a known command")

    return command[0]


def get_arguments(command: list[str], args) -> str:
    """
    Extract positional arguments from the command input.

    Maps positional arguments to their corresponding names based on the
    expected argument list. Raises an error if required arguments are missing.

    Args:
        command (list[str]): Remaining command input.
        args (list[str]): List of expected argument names.

    Returns:
        dict[str, str]: A dictionary mapping argument names to their values.

    Raises:
        Exception: If required arguments are missing.
    """
    if len(command) < len(args):
        raise Exception(f"[Error {ParseError.MISSING_ARGS}] "
                        "MISSING_ARGS: Missing arguments: "
                        f"{', '.join(args[len(command): len(args)])}")

    command_args = {}
    for index, value in enumerate(args):
        command_args[value] = command[index]

    return command_args


def get_flags(command: list[str], flags) -> str:
    """
    Parse and validate flags from the command input.

    Validates that flags exist in the defined configuration, maps short
    and long flag forms to canonical names, ensures flags are not repeated,
    and extracts their corresponding values.

    Args:
        command (list[str]): Remaining command input containing flags and values.
        flags (list[dict]): List of flag definitions, each containing:
            - "flag": list of aliases (e.g., ["-f", "--file"])
            - "name": canonical flag name

    Returns:
        dict[str, str]: A dictionary mapping canonical flag names to their values.

    Raises:
        Exception: If a flag is unknown or repeated.
    """
    # Define flag names that are valid
    valid_flags = []
    [valid_flags.extend(flag["flag"]) for flag in flags]

    # Define flags relation with name {-f: file}
    value = {}

    for flag in flags:
        name = flag["name"]
        for f in flag["flag"]:
            value[f] = name

    # Get the flag values

    command_flags = {}

    for i in range(0, len(command), 2):
        # Check the flag exists
        if command[i] not in valid_flags:
            raise Exception(f"[Error {ParseError.UNKNOWN_FLAGS}] "
                            f"UNKNOWN_FLAG: {command[i]} "
                            "flag isn't a valid flag")

        # Check the flag is not repeated
        if value[command[i]] in list(command_flags.keys()):
            raise Exception(f"[Error {ParseError.REPEATED_FLAG}] "
                            f'REPEATED_FLAG: the "{command[i]}" '
                            "flag was already defined")

        try:
            command_flags[value[command[i]]] = command[i + 1]
        except IndexError:
            print(f"[Error {ParseError.FLAG_WITHOUT_VALUE}] "
                    "FLAG_WITHOUT_VALUE: there wasn't a value "
                    f"assigned for {command[i]} flag")

    return command_flags
