import os
import constants
from utility import int_to_table_coordinate, replace_substring_in_string_from_index


def generate_empty_table(table_rows: int, table_columns: int) -> str:
    top = constants.TABLE_TOP_LEFT_CORNER + (constants.TABLE_TOP_BOTTOM * 3 + constants.TABLE_TOP_WITH_WALL_PLACEHOLDER) * \
        (table_columns - 1) + constants.TABLE_TOP_BOTTOM * \
        3 + constants.TABLE_TOP_RIGHT_CORNER + constants.NEW_LINE

    field_middle_part = constants.TABLE_SIDE + constants.TABLE_FIELD + (constants.TABLE_VERTICAL_WALL_PLACEHOLDER + constants.TABLE_FIELD) * \
        (table_columns - 1) + constants.TABLE_SIDE + constants.NEW_LINE

    field_bottom_part = constants.TABLE_SIDE_WITH_RIGHT_WALL_PLACEHOLDER + (constants.TABLE_HORIZONTAL_WALL_PLACEHOLDER * 3 + constants.TABLE_WALL_PLACEHOLDER_INTERSECTION) * \
        (table_columns - 1) + constants.TABLE_HORIZONTAL_WALL_PLACEHOLDER * \
        3 + constants.TABLE_SIDE_WITH_LEFT_WALL_PLACEHOLDER + constants.NEW_LINE

    bottom = constants.TABLE_BOTTOM_LEFT_CORNER + \
        (constants.TABLE_TOP_BOTTOM * 3 +
         constants.TABLE_BOTTOM_WITH_WALL_PLACEHOLDER) * (table_columns - 1) + 3 * constants.TABLE_TOP_BOTTOM + constants.TABLE_BOTTOM_RIGHT_CORNER + constants.NEW_LINE

    return top + (field_middle_part + field_bottom_part) * (table_rows - 1) + field_middle_part + bottom


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


def show_table(table_rows: int,
               table_columns: int,
               vertical_walls: list[tuple[int, int]],
               horizontal_walls: list[tuple[int, int]],
               pawn_x1: tuple[int, int],
               pawn_x2: tuple[int, int],
               pawn_o1: tuple[int, int],
               pawn_o2: tuple[int, int],
               start_positions_x: list[tuple[int, int]],
               start_positions_o: list[tuple[int, int]]) -> None:
    table = generate_empty_table(table_rows, table_columns)

    for vertical_wall in vertical_walls:
        table = add_vertical_wall(table, table_columns,
                                  vertical_wall[0], vertical_wall[1])

    for horizontal_wall in horizontal_walls:
        table = add_horizontal_wall(table, table_columns,
                                    horizontal_wall[0], horizontal_wall[1])

    table = add_start_position(table, table_columns,
                               start_positions_x[0][0], start_positions_x[0][1], True)
    table = add_start_position(table, table_columns,
                               start_positions_x[1][0], start_positions_x[1][1], True)
    table = add_start_position(table, table_columns,
                               start_positions_o[0][0], start_positions_o[0][1], False)
    table = add_start_position(table, table_columns,
                               start_positions_o[1][0], start_positions_o[1][1], False)

    table = add_pawn(table, table_columns,
                     pawn_x1[0], pawn_x1[1], True)
    table = add_pawn(table, table_columns,
                     pawn_x2[0], pawn_x2[1], True)
    table = add_pawn(table, table_columns,
                     pawn_o1[0], pawn_o1[1], False)
    table = add_pawn(table, table_columns,
                     pawn_o2[0], pawn_o2[1], False)

    clear_console()
    print_table(table, table_rows, table_columns)


def print_table(table: str, table_rows: int, table_columns: int) -> None:
    row_to_print = 2 * constants.SPACE

    for j in range(table_columns):
        row_to_print += constants.TABLE_FIELD + int_to_table_coordinate(j)
    row_to_print += constants.NEW_LINE

    row_size = 4 * table_columns + 2
    row_to_print += constants.TABLE_FIELD + table[:row_size]

    for i in range(table_rows * 2):
        num = int_to_table_coordinate(i // 2)
        if i % 2 == 0:
            row_to_print += constants.SPACE + num + constants.SPACE + \
                table[row_size * (i + 1): row_size * (i + 2) - 1] + \
                constants.SPACE + num + constants.NEW_LINE
        else:
            row_to_print += constants.TABLE_FIELD + \
                table[row_size * (i + 1): row_size * (i + 2)]

    row_to_print += constants.SPACE
    for j in range(table_columns):
        row_to_print += constants.TABLE_FIELD + int_to_table_coordinate(j)

    print(constants.NEW_LINE + row_to_print + constants.NEW_LINE)


def calculate_position_for_insertion(table_columns: int, row: int, column: int, row_modifier: int = 0) -> int:
    return 4 * (table_columns * (row + row_modifier) + column +
                row - 1 + table_columns * (row - 1))


def add_pawn(table: str, table_columns: int, row: int, column: int, is_X: bool) -> str:
    return replace_substring_in_string_from_index(table, calculate_position_for_insertion(table_columns, row, column), constants.TABLE_X if is_X else constants.TABLE_Y)


def add_start_position(table: str, table_columns: int, row: int, column: int, is_X: bool) -> str:
    return replace_substring_in_string_from_index(table, calculate_position_for_insertion(table_columns, row, column), constants.TABLE_START_POSITION_X if is_X else constants.TABLE_START_POSITION_Y)


def move_pawn(table: str, table_columns: int, old_row: int, old_column: int, new_row: int, new_column: int) -> str:
    pawn_position = calculate_position_for_insertion(
        table_columns, old_row, old_column)
    pawn = table[pawn_position: pawn_position + 1]
    temp_table = replace_substring_in_string_from_index(
        table, pawn_position, constants.SPACE)

    pawn_position = calculate_position_for_insertion(
        table_columns, new_row, new_column)
    return replace_substring_in_string_from_index(temp_table, pawn_position, pawn)


def show_end_screen(computer_on_move: bool) -> bool:
    print(f'{"Computer" if not computer_on_move else "Player"} won!')
    return read_yes_no_prefered("Play again", False)


def show_start_screen() -> None:
    resize_terminal(27, 80)
    print("Welcome to Blockade! :)")


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def resize_terminal(height: int, width: int) -> None:
    os.system(f"mode con: cols={width} lines={height}" if os.name ==
              'nt' else f"printf '\e[8;{height};{width}t'")


def read_move() -> list():  # to implament phase 2
    return


def read_first_player() -> bool:
    return read_yes_no_prefered("Computer plays first", False)


def read_table_size() -> tuple[int, int]:
    return (read_int_from_range_and_prefered("rows", 3, 23, 11), read_int_from_range_and_prefered("columns", 4, 28, 14))


def read_wall_count() -> int:
    return read_int_from_range_and_prefered("walls", 0, 18, 9)


def read_start_positions(table_rows: int, table_columns: int) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    # tuple[int, int] je pozicija jednog pesaka
    first_player_1 = input_pawn_position(
        "first player first pawn", table_rows, table_columns, 4, 3, [])
    first_player_2 = input_pawn_position(
        "first player second pawn", table_rows, table_columns, 4, 4, [first_player_1])

    second_player_1 = input_pawn_position(
        "second player first pawn", table_rows,  table_columns, 5, 3, [first_player_1, first_player_2])
    second_player_2 = input_pawn_position("second player second pawn", table_rows, table_columns,  5, 4, [
        first_player_1, first_player_2, second_player_1])

    return [(first_player_1, first_player_2), (second_player_1, second_player_2)]


def input_pawn_position(what_player: str,  table_rows: int, table_columns: int, prefered_column: int, prefered_row: int, busy_positions) -> tuple[int, int]:
    row = read_int_from_range_and_prefered(
        what_player+" start row", 0, table_rows, prefered_row if table_rows > prefered_row else table_rows)
    column = read_int_from_range_and_prefered(
        what_player+" start column", 0, table_columns, prefered_column if table_columns > prefered_column else table_columns)
    return (row, column) if (row, column) not in busy_positions else print("Enter again") or input_pawn_position(what_player, table_rows, table_columns,  prefered_column, prefered_row, busy_positions)


def read_yes_no_prefered(question: str, prefered_yes: bool) -> bool:
    allowed_answers = ["Y", "YES", "YE", " ", "", "NO", "N"]
    val = None
    while val not in allowed_answers:
        val = input(
            question+(" [YES/no]: " if prefered_yes else " [yes/NO]: "))
        val = str.upper(val)
    return val in allowed_answers[:5] if prefered_yes else val in allowed_answers[:3]

def read_int_from_range_and_prefered(what_to_read: str, low: int, high: int, prefered: int) -> int:
    if low == high:
        return low
    if low > high:
        pom = low
        low = high
        high = pom
    if prefered < low or prefered > high:
        return False
    while True:
        pom = input(what_to_read+"["+str(prefered)+"]: ")
        if pom == "" or pom == " ":
            pom = prefered
            break
        if pom.strip().isdigit():
            pom = int(pom)
            if pom >= low and pom <= high:
                break
            print("You must enter number between "+str(low)+" and "+str(high))
        else:
            print("You must enter whole number")
    return pom
