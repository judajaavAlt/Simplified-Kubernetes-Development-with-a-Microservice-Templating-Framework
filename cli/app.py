from .userInterface.command_line_interface import get_args
from .presentation.command_parser import parse_command
from .infraestructure.sqlite_adapter import SQLiteDatabaseHandler
from .application.config import Config

def main():
    config = Config()
    database = SQLiteDatabaseHandler()
    database.connect()
    console_input = get_args()

    parsed_command = parse_command(console_input)

    if parsed_command is None:
        return 1

    command, args = parsed_command
    database.close()
    return 0
