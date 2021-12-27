from constants import COORDINATES


def str_to_coordinate(val: chr) -> tuple[int, int]:
    if val.strip().isdigit():
        return int(val)
    return ord(val)-55


def int_to_table_coordinate(int: int) -> str:
    return COORDINATES[int % len(COORDINATES)]


def replace_substring_in_string_from_index(str: str, start_index: int, substr: str) -> str:
    return str[:start_index] + substr + str[start_index + len(substr):]


def check_if_string_is_number_in_range(str: str, low: int, high: int) -> int | None:
    if str.strip().isdigit():
        str = int(str)
        if str >= low and str <= high:
            return str
    return None
