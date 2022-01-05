from constants import COORDINATES


def table_coordinate_to_int(table_coordinate: str) -> int:
    if len(table_coordinate) > 1 or table_coordinate not in COORDINATES:
        return -1

    return COORDINATES.index(table_coordinate) + 1


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


def update_tuple(tuple_to_update: tuple, index_to_update: int, new_value) -> tuple:
    tuple_list = list(tuple_to_update)
    tuple_list[index_to_update] = new_value
    return tuple(tuple_list)


def add_to_tuple(tuple_to_update: tuple, new_value) -> tuple:
    tuple_list = list(tuple_to_update)
    tuple_list.append(new_value)
    return tuple(tuple_list)
