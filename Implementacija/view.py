from types import NoneType
from typing import Tuple


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


def read_first_player():
    allowed_answers = ["Y","YES","YE", " ","","NO","N"]
    val=None
    while val not in allowed_answers:
        val=input("Computer plays first?[YES/no]")
        val=str.upper(val)
    return True if val in allowed_answers[:5] else False

def read_table_size()->tuple[int,int]:
    while True:
        row=input("Number of rows:[14]")
        if row=="" or row==" ":
            row=14
            break
        if row.strip().isdigit():
            row=int(row)
            if row >=4 and row <=28 and row%2==0:
                break
            print("You must enter number between 4 and 28")
        else:
            print("You must enter number")
    while True:
        column=input("Number of column:[11]")
        if column=="" or column==" ":
            column=11
            break
        if column.strip().isdigit():
            column=int(column)
            if column >=3 and column <=23 and column%2==1:
                break
            print("You must enter number between 3 and 23")
        else:
            print("You must enter number")   
    return (row,column)


def read_wall_count():
    return


def read_start_positions():
    return
