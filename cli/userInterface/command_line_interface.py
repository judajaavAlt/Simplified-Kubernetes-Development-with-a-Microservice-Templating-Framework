import sys


def get_args() -> str:
    return sys.argv


def output_message(message: str) -> None:
    print(message)


def output_error(exception_type: Exception,
                 exception_message: str) -> None:
    raise exception_type(exception_message)
