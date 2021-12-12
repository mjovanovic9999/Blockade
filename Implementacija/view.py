from types import NoneType
from typing import Tuple

from utility import int_to_table_coordinate


def generate_empty_table( table_rows: int,table_columns: int) -> str:
    start = "\u2554"+("\u2550"*3+"\u2564") * \
        (table_columns-1) + "\u2550"*3+"\u2557\n"

    middle_box = "\u2551   "+"\u2502   "*(table_columns-1) + "\u2551\n"

    down_box = "\u255F"+("\u2500"*3+"\u253C") * \
        (table_columns-1)+"\u2500\u2500\u2500\u2562\n"

    end = "\u255A"+("\u2550"*3+"\u2567")*(table_columns-1) + \
        "\u2550\u2550\u2550\u255D\n"

    return start+(middle_box+down_box)*(table_rows-1)+middle_box+end


def add_vertical_wall(table: str,  table_rows: int,table_columns: int, row: int, column: int) -> str:
    pom = 4*(table_columns*(row)+column+row-1+table_columns*(row-1))+2
    temp = table[:pom]+"\u2503"+table[pom+1:]
    pom += table_columns*4+2
    temp = temp[:pom]+"\u2542"+temp[pom+1:]
    pom += table_columns*4+2
    return temp[:pom]+"\u2503"+temp[pom+1:]


def add_horizontal_wall(table: str,  table_rows: int ,table_columns: int, row: int, column: int) -> str:
    pom = 4*(table_columns*(row+1)+column+row-1+table_columns*(row-1))+2
    temp = table[:pom-1]+"\u2501"*3+table[pom+2:]
    pom += 2
    temp = temp[:pom]+"\u253f"+temp[pom+1:]
    pom += 1
    return temp[:pom]+"\u2501"*3+table[pom+3:]


def print_table_from_dict(state:dict[str,tuple[int,int,int]],table_rows: int, table_columns: int):
    return


def print_table(table: str, table_rows: int, table_columns: int) -> None:
    print(" ", end="")
    for j in range(table_columns):
        print("   "+(str(j+1) if j < 9 else chr(65-9+j)) + "", end="")
    print("")
    size = 4*table_columns+2
    print("  "+table[0:size], end="")
    for i in range(table_rows*2):
        num = int_to_table_coordinate(i//2)
        if i % 2 == 0:
            print("" + num + " ", end="")
            print(table[size*(i+1):size*(i+2)-1]+" "+num+"\n", end="")
        else:
            print("  ", end="")
            print(table[size*(i+1):size*(i+2)], end="")

    print(" ", end="")
    for j in range(table_columns):
        print("   "+(str(j+1) if j < 9 else chr(65-9+j)) + "", end="")

    print("")

    return


def add_pawn(table: str, table_rows: int, table_columns: int, row: int, column: int, is_X: bool) -> str:
    pom = 4*(table_columns*(row)+column+row-1+table_columns*(row-1))
    return table[:pom]+("X" if is_X else "O")+table[pom+1:]


def add_start_position(table: str, table_rows: int, table_columns: int, row: int, column: int, is_X: bool) -> str:
    pom = 4*(table_columns*(row)+column+row-1+table_columns*(row-1))
    return table[:pom]+("\u24cd" if is_X else "\u24c4")+table[pom+1:]


def move_pawn(table: str,  table_rows: int, table_columns: int, old_row: int, old_column: int, new_row: int, new_column: int) -> str:
    pom = 4*(table_columns*(old_row)+old_column+old_row-1+table_columns*(old_row-1))
    pawn = table[pom:pom+1]
    temp = table[:pom]+" "+table[pom+1:]
    pom = 4*(table_columns*(new_row)+new_column+new_row-1+table_columns*(new_row-1))
    return temp[:pom]+pawn+table[pom+1:]


def show_end_screen() -> bool:
    return read_yes_no_prefered("Play again", False)


def show_start_screen():
    print("Welcome to Blockade! :)")
    return


def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    return


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
    if prefered_yes:
        return True if val in allowed_answers[:5] else False
    else:
        return True if val in allowed_answers[:3] else False


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
