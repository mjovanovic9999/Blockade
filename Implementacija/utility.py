from queue import Queue
from typing import List, Set
from constants import COORDINATES


def table_coordinate_to_int(table_coordinate: str) -> int:
    if len(table_coordinate) > 1 or table_coordinate not in COORDINATES:
        return -1

    return COORDINATES.index(table_coordinate) + 1


def int_to_table_coordinate(int: int) -> str:
    return COORDINATES[(int - 1) % len(COORDINATES)]


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


def update_pawn_positions(
    old_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    selected_player_index: int,
    selected_pawn_index: int,
    new_pawn_position:tuple[int,int],
    ) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    tuple_list = list(old_positions[selected_player_index])
    tuple_list[selected_pawn_index] = new_pawn_position
    return (old_positions[0],tuple(tuple_list)) if selected_player_index else (tuple(tuple_list),old_positions[1])

def add_wall_in_tuple(
    walls:tuple[tuple[tuple[int,int],...], tuple[tuple[int,int], ...]],
    new_wall:tuple[int,int],
    is_wall_horizontal:bool,
    )->tuple[tuple[tuple[int,int],...], tuple[tuple[int,int], ...]]:
    updated_walls=list(walls[is_wall_horizontal])
    updated_walls.append(new_wall)
    return (walls[0],updated_walls) if is_wall_horizontal else (updated_walls,walls[1])
    

def decrement_number_of_walls(
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    selected_player_index: int,
    is_wall_horizontal:bool
    )->tuple[tuple[int, int], tuple[int, int]]:
    veritcal,horizontal=number_of_walls[selected_player_index]
    if is_wall_horizontal:
        horizontal-=1
    else:
        veritcal-=1
    return (number_of_walls[0],(veritcal,horizontal)) if selected_player_index else ((veritcal,horizontal),number_of_walls[1])


def add_to_tuple(tuple_to_update: tuple, new_value) -> tuple:
    tuple_list = list(tuple_to_update)
    tuple_list.append(new_value)
    return tuple(tuple_list)


def tuple_4_positions(
    first1row: int, first1column, first2row: int, first2column: int,
    second1row: int, second1column: int, second2row: int, second2column: int
    ) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    return (((first1row, first1column), (first2row, first2column)), ((second1row, second1column), (second2row, second2column)))
