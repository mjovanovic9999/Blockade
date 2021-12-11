from types import NoneType
from typing import Tuple
from utility import read_int_from_range_and_prefered, read_yes_no_prefered, read_pawn_position


def show_table():
    return


def show_end_screen():
    # igraj opet
    return


def show_start_screen():
    return


def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def read_move() -> list():
    return


def read_first_player() -> bool:
    return read_yes_no_prefered("Computer plays first", False)


def read_table_size() -> tuple[int, int]:
    return (read_int_from_range_and_prefered("columns", 4, 28, 14), read_int_from_range_and_prefered("rows", 3, 23, 11))


def read_wall_count() -> int:
    return read_int_from_range_and_prefered("walls", 0, 18, 9)


def read_start_positions(table_columns: int, table_rows: int) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:

    first_player_1 = read_pawn_position(
        "first player first pawn", table_columns, table_rows, 4, 4, [])
    first_player_2 = read_pawn_position(
        "first player second pawn", table_columns, table_rows, 4, 4, [first_player_1])

    second_player_1 = read_pawn_position(
        "second player first pawn", table_columns, table_rows, 4, 4, [first_player_1, first_player_2])
    second_player_2 = read_pawn_position("second player second pawn", table_columns, table_rows, 4, 4, tuple[
                                         first_player_1, first_player_2, second_player_1])

    return [(first_player_1, first_player_2), (second_player_1, second_player_2)]
