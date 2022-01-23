import os
import constants
from moves import move_pawn, place_wall
from utility import check_if_string_is_number_in_range, int_to_table_coordinate, replace_substring_in_string_from_index, table_coordinate_to_int, update_tuple
from frozendict import frozendict


def generate_empty_table(table_size: tuple[int, int]) -> str:
    top = constants.TABLE_TOP_LEFT_CORNER + (constants.TABLE_TOP_BOTTOM * 3 + constants.TABLE_TOP_WITH_WALL_PLACEHOLDER) * \
        (table_size[1] - 1) + constants.TABLE_TOP_BOTTOM * \
        3 + constants.TABLE_TOP_RIGHT_CORNER + constants.NEW_LINE

    field_middle_part = constants.TABLE_SIDE + constants.TABLE_FIELD + (constants.TABLE_VERTICAL_WALL_PLACEHOLDER + constants.TABLE_FIELD) * \
        (table_size[1] - 1) + constants.TABLE_SIDE + constants.NEW_LINE

    field_bottom_part = constants.TABLE_SIDE_WITH_RIGHT_WALL_PLACEHOLDER + (constants.TABLE_HORIZONTAL_WALL_PLACEHOLDER * 3 + constants.TABLE_WALL_PLACEHOLDER_INTERSECTION) * \
        (table_size[1] - 1) + constants.TABLE_HORIZONTAL_WALL_PLACEHOLDER * \
        3 + constants.TABLE_SIDE_WITH_LEFT_WALL_PLACEHOLDER + constants.NEW_LINE

    bottom = constants.TABLE_BOTTOM_LEFT_CORNER + \
        (constants.TABLE_TOP_BOTTOM * 3 +
         constants.TABLE_BOTTOM_WITH_WALL_PLACEHOLDER) * (table_size[1] - 1) + 3 * constants.TABLE_TOP_BOTTOM + constants.TABLE_BOTTOM_RIGHT_CORNER + constants.NEW_LINE

    return top + (field_middle_part + field_bottom_part) * (table_size[0] - 1) + field_middle_part + bottom


def add_vertical_wall(table: str, table_columns: int, row: int, column: int) -> str:
    wall_position = calculate_position_for_insertion(
        table_columns, row, column) + 2

    temp_table = table[:wall_position] + \
        constants.TABLE_VERTICAL_WALL + table[wall_position + 1:]

    for wall_symbol in [constants.TABLE_VERTICAL_WALL_INTERSECTION, constants.TABLE_VERTICAL_WALL]:
        wall_position += table_columns * 4 + 2
        temp_table = replace_substring_in_string_from_index(
            temp_table, wall_position, wall_symbol)

    return temp_table


def add_horizontal_wall(table: str, table_columns: int, row: int, column: int) -> str:
    wall_position = calculate_position_for_insertion(
        table_columns, row, column, 1) + 1

    return replace_substring_in_string_from_index(table, wall_position, 3 * constants.TABLE_HORIZONTAL_WALL + constants.TABLE_HORIZONTAL_WALL_INTERSECTION + 3 * constants.TABLE_HORIZONTAL_WALL)


def show_table(table_size: tuple[int, int],
               walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
               current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
               start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]) -> None:
    table = generate_empty_table(table_size)

    for vertical_wall in walls[0]:
        table = add_vertical_wall(table, table_size[1],
                                  vertical_wall[0], vertical_wall[1])

    for horizontal_wall in walls[1]:
        table = add_horizontal_wall(table, table_size[1],
                                    horizontal_wall[0], horizontal_wall[1])

    table = add_start_position(table, table_size[1],
                               start_positions[0][0][0], start_positions[0][0][1], True)
    table = add_start_position(table, table_size[1],
                               start_positions[0][1][0], start_positions[0][1][1], True)
    table = add_start_position(table, table_size[1],
                               start_positions[1][0][0], start_positions[1][0][1], False)
    table = add_start_position(table, table_size[1],
                               start_positions[1][1][0], start_positions[1][1][1], False)

    table = add_pawn(table, table_size[1],
                     current_pawn_positions[0][0][0], current_pawn_positions[0][0][1], True)
    table = add_pawn(table, table_size[1],
                     current_pawn_positions[0][1][0], current_pawn_positions[0][1][1], True)
    table = add_pawn(table, table_size[1],
                     current_pawn_positions[1][0][0], current_pawn_positions[1][0][1], False)
    table = add_pawn(table, table_size[1],
                     current_pawn_positions[1][1][0], current_pawn_positions[1][1][1], False)

    clear_console()
    print_table(table, table_size)


def print_table(table: str, table_size: tuple[int, int]) -> None:
    row_to_print = 2 * constants.SPACE

    for j in range(1, table_size[1] + 1):
        row_to_print += constants.TABLE_FIELD + int_to_table_coordinate(j)
    row_to_print += constants.NEW_LINE

    row_size = 4 * table_size[1] + 2
    row_to_print += constants.TABLE_FIELD + table[:row_size]

    for i in range(1, table_size[0] * 2 + 1):
        num = int_to_table_coordinate(i // 2 + 1)
        if i % 2 == 1:
            row_to_print += constants.SPACE + num + constants.SPACE + \
                table[row_size * i: row_size * (i + 1) - 1] + \
                constants.SPACE + num + constants.NEW_LINE
        else:
            row_to_print += constants.TABLE_FIELD + \
                table[row_size * i: row_size * (i + 1)]

    row_to_print += 2 * constants.SPACE
    for j in range(1, table_size[1] + 1):
        row_to_print += constants.TABLE_FIELD + int_to_table_coordinate(j)

    print(constants.NEW_LINE + row_to_print + constants.NEW_LINE)


def calculate_position_for_insertion(table_columns: int, row: int, column: int, row_modifier: int = 0) -> int:
    return 4 * (table_columns * (row + row_modifier) + column +
                row - 1 + table_columns * (row - 1))


def add_pawn(table: str, table_columns: int, row: int, column: int, is_X: bool) -> str:
    return replace_substring_in_string_from_index(table, calculate_position_for_insertion(table_columns, row, column),
                                                  constants.TABLE_X if is_X else constants.TABLE_O)


def add_start_position(table: str, table_columns: int, row: int, column: int, is_X: bool) -> str:
    return replace_substring_in_string_from_index(table, calculate_position_for_insertion(table_columns, row, column),
                                                  constants.TABLE_START_POSITION_X if is_X else constants.TABLE_START_POSITION_Y)


def move_pawn_on_table(table: str,
                       table_columns: int,
                       old_row: int,
                       old_column: int,
                       new_row: int,
                       new_column: int) -> str:
    pawn_position = calculate_position_for_insertion(
        table_columns, old_row, old_column)
    pawn = table[pawn_position: pawn_position + 1]
    temp_table = replace_substring_in_string_from_index(
        table, pawn_position, constants.SPACE)

    pawn_position = calculate_position_for_insertion(
        table_columns, new_row, new_column)
    return replace_substring_in_string_from_index(temp_table, pawn_position, pawn)


def show_end_screen(computer_or_x_won: bool, player_vs_player: bool = True) -> bool:
    messages = (constants.MESSAGE_PLAYER_X_WON, constants.MESSAGE_PLAYER_O_WON) if player_vs_player else (
        constants.MESSAGE_COMPUTER_WON, constants.MESSAGE_PLAYER_WON)
    print(messages[0] if not computer_or_x_won else messages[1])
    return read_yes_no_prefered(constants.MESSAGE_PLAY_AGAIN, False)


def show_start_screen() -> None:
    print(constants.MESSAGE_WELCOME)


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def resize_terminal(height: int, width: int) -> None:
    os.system(f"mode con: cols={width} lines={height}" if os.name ==
              'nt' else f"printf '\e[8;{height};{width}t'")


def read_move(current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
              start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
              walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
              number_of_walls: tuple[tuple[int, int], tuple[int, int]],
              table_size: tuple[int, int],
              computer_or_x_to_move: bool,
              connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
              multiplayer: bool = True) -> tuple[tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]], tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]], tuple[tuple[int, int], tuple[int, int]]]:
    if multiplayer:
        print(constants.MESSAGE_PLAYER_X_TO_MOVE if computer_or_x_to_move else constants.MESSAGE_PLAYER_O_TO_MOVE)
    else:
        print("Player's turn")

    selected_player_index = 0 if computer_or_x_to_move else 1

    selected_pawn_index = read_selected_pawn(
        current_pawn_positions[selected_player_index])

    new_pawn_position = read_pawn_position_and_move_pawn(
        current_pawn_positions,
        start_positions,
        walls,
        table_size,
        selected_player_index,
        selected_pawn_index)

    selected_wall_index = read_selected_wall(
        number_of_walls[selected_player_index])

    if selected_wall_index != -1:
        new_wall_state = read_wall_position_and_place_wall(
            current_pawn_positions,
            start_positions,
            walls,
            number_of_walls,
            {},
            table_size,
            selected_wall_index,
            selected_player_index,
            connection_points
        )
        return (new_pawn_position, new_wall_state[0], new_wall_state[1])
    return (new_pawn_position, walls, number_of_walls)


def read_selected_wall(current_players_number_of_walls: tuple[int, int]) -> int:
    has_horizontal_walls_left = current_players_number_of_walls[1] > 0
    has_vertical_walls_left = current_players_number_of_walls[0] > 0
    if has_horizontal_walls_left and has_vertical_walls_left:
        return read_int_from_range_with_preferred_value_or_options_recursion(constants.MESSAGE_WALL_SELECTION, 1, 2, constants.MESSAGE_WALL_TYPES) - 1
    if has_horizontal_walls_left:
        print(constants.MESSAGE_HORIZONTAL_WALLS_REMAINING)
        return 1
    if has_vertical_walls_left:
        print(constants.MESSAGE_VERTICAL_WALLS_REMAINING)
        return 0
    print(constants.MESSAGE_NO_WALLS_REMAINING)
    return -1


def read_wall_position_and_place_wall(current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                                      start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                                      walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
                                      number_of_walls: tuple[tuple[int, int], tuple[int, int]],
                                      heat_map: dict[tuple[int, int], int],
                                      table_size: tuple[int, int],
                                      wall_index: int,
                                      player_index: int,
                                      connection_points: frozendict[tuple[int,
                                                                          int], tuple[tuple[int, int], ...]]
                                      ) -> tuple[tuple[tuple, tuple], tuple[tuple[int, int], tuple[int, int]], dict[tuple[int, int], int]]:
    wall_position = read_row_and_column(table_size,
                                        constants.MESSAGE_WALL_ROW,
                                        constants.MESSAGE_WALL_COLUMN)

    new_wall_state = place_wall(current_pawns_positions,
                                start_positions,
                                walls,
                                number_of_walls,
                                heat_map,
                                table_size,
                                wall_position,
                                wall_index,
                                player_index,
                                connection_points)

    if new_wall_state != (walls, number_of_walls, heat_map):
        return new_wall_state

    print(constants.MESSAGE_INVALID_WALL_POSITION)
    return read_wall_position_and_place_wall(
        current_pawns_positions,
        start_positions,
        walls,
        number_of_walls,
        heat_map,
        table_size,
        wall_index,
        player_index,
        connection_points
    )


def read_row_and_column(table_size: tuple[int, int],
                        row_message: str,
                        column_message: str) -> tuple[int, int]:
    new_position_row = read_coordinate(row_message, table_size[0])
    new_position_column = read_coordinate(column_message, table_size[1])
    return (new_position_row, new_position_column)


def read_selected_pawn(current_players_pawn_positions: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return read_int_from_range_with_preferred_value_or_options_recursion(constants.MESSAGE_PAWN_SELECTION, 1, 2, f'1 => ({int_to_table_coordinate(current_players_pawn_positions[0][0])}, {int_to_table_coordinate(current_players_pawn_positions[0][1])}) / 2 => ({int_to_table_coordinate(current_players_pawn_positions[1][0])}, {int_to_table_coordinate(current_players_pawn_positions[1][1])})') - 1


def read_pawn_position_and_move_pawn(current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                                     start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                                     walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
                                     table_size: tuple[int, int],
                                     selected_player_index: int,
                                     selected_pawn_index: int,
                                     ) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:

    new_pawn_position = read_row_and_column(
        table_size, constants.MESSAGE_PAWN_NEW_ROW, constants.MESSAGE_PAWN_NEW_COLUMN)

    new_pawn_positions = move_pawn(current_pawn_positions,
                                   start_positions,
                                   new_pawn_position,
                                   walls,
                                   table_size,
                                   selected_player_index,
                                   selected_pawn_index)
    if new_pawn_positions != current_pawn_positions:
        return new_pawn_positions

    print(constants.MESSAGE_INVALID_PAWN_MOVE)
    return read_pawn_position_and_move_pawn(current_pawn_positions,
                                            start_positions,
                                            walls,
                                            table_size,
                                            selected_player_index,
                                            selected_pawn_index)


def read_first_player() -> bool:
    return read_yes_no_prefered(constants.MESSAGE_COMPUTER_PLAYS_FIRST, True)


def read_game_mode() -> bool:
    return read_yes_no_prefered(constants.MESSAGE_PLAY_VS_COMPUTER, True)


def read_table_size() -> tuple[int, int]:
    return (read_int_from_range_with_preferred_value(constants.MESSAGE_NUMBER_OF_ROWS, 3, 23, 11),
            read_int_from_range_with_preferred_value(constants.MESSAGE_NUMBER_OF_COLUMNS, 4, 28, 14))


def read_wall_count() -> tuple[tuple[int, int], tuple[int, int]]:
    number_of_walls = read_int_from_range_with_preferred_value(
        constants.MESSAGE_NUMBER_OF_WALLS, 0, 18, 9)
    return ((number_of_walls, number_of_walls), (number_of_walls, number_of_walls))


def read_start_positions(table_size: tuple[int, int]) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    # tuple[int, int] je pozicija jednog pesaka
    player_x_first_pawn = read_pawn_start_position(
        constants.MESSAGE_PLAYER_X_FIRST_PAWN, table_size, 4, 4, [])
    player_x_second_pawn = read_pawn_start_position(
        constants.MESSAGE_PLAYER_X_SECOND_PAWN, table_size, 8, 4, [player_x_first_pawn])

    player_o_first_pawn = read_pawn_start_position(
        constants.MESSAGE_PLAYER_O_FIRST_PAWN, table_size, 4, 11, [player_x_first_pawn, player_x_second_pawn])
    player_o_second_pawn = read_pawn_start_position(constants.MESSAGE_PLAYER_O_SECOND_PAWN, table_size,  8, 11, [
        player_x_first_pawn, player_x_second_pawn, player_o_first_pawn])

    return [(player_x_first_pawn, player_x_second_pawn), (player_o_first_pawn, player_o_second_pawn)]


def read_pawn_start_position(which_player: str,
                             table_size: tuple[int, int],
                             prefered_row: int,
                             prefered_column: int,
                             occupied_positions) -> tuple[int, int]:
    row = read_int_from_range_with_preferred_value(
        which_player + " start row", 1, table_size[0], prefered_row)
    column = read_int_from_range_with_preferred_value(
        which_player + " start column", 1, table_size[1], prefered_column)
    return (row, column) if (row, column) not in occupied_positions else print(f'{constants.MESSAGE_INVALID_PAWN_POSITION} ({table_size[0]}x{table_size[1]})') or read_pawn_start_position(which_player, table_size,  prefered_column, prefered_row, occupied_positions)


def read_yes_no_prefered(question: str, prefered_yes: bool) -> bool:
    allowed_answers = ["Y", "YES", "YE", " ", "", "NO", "N"]
    val = None
    while val not in allowed_answers:
        val = input(
            question + (" [YES/no]: " if prefered_yes else " [yes/NO]: "))
        val = str.upper(val)
    return val in allowed_answers[:5] if prefered_yes else val in allowed_answers[:3]


def read_int_from_range_with_preferred_value(what_to_read: str, low: int, high: int, preferred: int) -> int:
    if low == high:
        return low

    if low > high:
        temp = low
        low = high
        high = temp

    if preferred < low:
        preferred = low

    elif preferred > high:
        preferred = high

    return read_int_from_range_with_preferred_value_or_options_recursion(what_to_read, low, high, preferred)


def read_int_from_range_with_preferred_value_or_options_recursion(what_to_read: str,
                                                                  low: int,
                                                                  high: int,
                                                                  preferred_or_options: int | str | None = None) -> int:
    message = what_to_read
    include_preferred = isinstance(preferred_or_options, int)

    if preferred_or_options:
        message += f' [{str(preferred_or_options) if include_preferred else preferred_or_options}]'

    message += ": "
    temp = input(message)

    if include_preferred and (temp == "" or temp == " "):
        return preferred_or_options

    temp_int = check_if_string_is_number_in_range(temp, low, high)
    if temp_int != None:
        return temp_int

    print(f'{constants.MESSAGE_INVALID_NUMBER_INPUT} ({low} - {high})')
    return read_int_from_range_with_preferred_value_or_options_recursion(what_to_read,
                                                                         low,
                                                                         high,
                                                                         preferred_or_options)


def read_coordinate(message: str, high: int) -> int:
    coordinate = table_coordinate_to_int(input(message + ": ").upper())
    if coordinate > 0 and coordinate <= high:
        return coordinate
    print(constants.MESSAGE_INVALID_COORDINATE)
    return read_coordinate(message, high)
