"""
This module contains a set of constant related with status information for
outputs
"""


class Basic:
    """statuses for default results"""
    SUCCESS = 0
    """status when an action goes as intended"""

    ERROR = 1
    """status when an unexpected error happens"""


class ParseError:
    """Error statuses for the cli/presentantion/command_parser module"""

    NO_COMMAND = 2
    """status when couldn't find a command"""

    UNKNOWN_COMMAND = 3
    """status when a command was found but not recognized"""

    MISSING_ARGS = 4
    """status when couldn't find a command arguments"""

    UNKNOWN_FLAGS = 5
    """status when the flag isn't recognized"""

    REPEATED_FLAG = 6
    """status when the flag isn't recognized"""
    
    FLAG_WITHOUT_VALUE = 7
    """status when the flag isn't recognized"""
