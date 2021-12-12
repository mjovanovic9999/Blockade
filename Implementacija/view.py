from types import NoneType
from typing import Tuple
from utility import read_int_from_range_and_prefered, read_yes_no_prefered, read_pawn_position


# def show_table(table_columns: int, table_rows: int, pawns_x: tuple[tuple[int, int], tuple[int, int]], pawns_o: tuple[tuple[int, int], tuple[int, int]], vertical_walls: list[tuple[int, int]], horisontal_walls: list[tuple[int, int]]) -> str:
    
   
   
#     table = "   "
#     for i in range(table_columns+4):
#         for j in range(table_rows+4):
#             if i == 0:
#                 table += (str(j+1) if j < 9 else chr(65-9+j)) + " "
#                 if j == table_rows-1:
#                     table += "  \n"
#                     break
#             elif i == 1:
#                 if j == 0:
#                     table += "   "
#                 table += "\u003d "
#                 if j == table_rows-1:
#                     table += "   \n"
#                     break
#             elif i == table_columns+2:
#                 if j == 0:
#                     table += "  "
#                 table += " \u003d"
#                 if j == table_rows-1:
#                     table += "   \n"
#                     break
#             elif i == table_columns+3:
#                 if j == 0:
#                     table += "   "
#                 table += (str(j+1) if j < 9 else chr(65-9+j)) + " "
#                 if j == table_rows-1:
#                     table += "  \n"
#                     break

#             elif j == 0:
#                 table += (str(i-1) if i < 9 else chr(65-9+i)) + " \u2551"
#             elif j == table_rows:
#                 table += " \u2551 "+(str(i-1) if i < 9 else chr(65-9+i))+"\n"
#                 table += ("  "+" \u2014"*table_rows +"\n" )if i != table_columns+1 else ""
#                 break
#             else:
#                 if pawns_x[0][0] == i and pawns_x[0][1] == j or pawns_x[1][0] == i and pawns_x[1][1] == j:
#                     table += "X"
#                 elif pawns_o[0][0] == i and pawns_o[0][1] == j or pawns_o[1][0] == i and pawns_o[1][1] == j:
#                     table += "O"
#                 else:
#                     table += " "
#                 if (i-1, j) in vertical_walls:
#                     table += "\u2551"
#                 else:
#                     table += "|"

#     return table


def generate_empty_table(table_columns: int, table_rows: int) -> str:
    start="\u2554"+("\u2550"*3+"\u2564")*(table_columns-1) +"\u2550"*3+"\u2557\n"

    middle_box="\u2551   "+"\u2502   "*(table_columns-1)+   "\u2551\n"

    down_box="\u255F"+("\u2500"*3+"\u253C")*(table_columns-1)+"\u2500\u2500\u2500\u2562\n"

    end="\u255A"+("\u2550"*3+"\u2567")*(table_columns-1)+"\u2550\u2550\u2550\u255D\n"

    return start+(middle_box+down_box)*(table_rows-1)+middle_box+end



def add_vertical_wall(table:str,table_columns: int, table_rows: int,x:int,y:int):
    pom=4*(table_columns*(x)+y+x-1+table_columns*(x-1))+2
    temp= table[:pom]+"\u2503"+table[pom+1:]
    pom+=table_columns*4+2
    temp=temp[:pom]+"\u2542"+temp[pom+1:]
    pom+=table_columns*4+2
    return temp[:pom]+"\u2503"+temp[pom+1:]



def add_horizontal_wall(table:str,table_columns: int, table_rows: int,x:int,y:int):
    pom=4*(table_columns*(x+1)+y+x-1+table_columns*(x-1))+2
    temp= table[:pom-1]+"\u2501"*3+table[pom+2:]
    pom+=2
    temp= temp[:pom]+"\u253f"+temp[pom+1:]
    pom+=1
    return temp[:pom]+"\u2501"*3+table[pom+3:]

def print_table(table:str,table_columns: int, table_rows: int)->None:
    print(" ",end="")
    for j in range(table_columns):
        print("   "+(str(j+1) if j < 9 else chr(65-9+j)) + "",end="")
    print("")
    size=4*table_columns+2
    print("  "+table[0:size],end="")
    for i in range(table_rows*2):
        num=(str(i//2+1) if i//2 < 9 else chr(65-9+i//2))
        if i%2==0:
            print(""+ num+ " ",end="")
            print(table[size*(i+1):size*(i+2)-1]+" "+num+"\n",end="")
        else:
            print("  ",end="")
            print(table[size*(i+1):size*(i+2)],end="")

    print(" ",end="")
    for j in range(table_columns):
        print("   "+(str(j+1) if j < 9 else chr(65-9+j)) + "",end="")
    
    print("")

    return

# def move_pawn(table:str,table_columns: int, table_rows: int,x:int,y:int,new_x:int,new_y:int):
#     pom=4*(table_columns+x*table_rows+y)
#     pawn=table[pom]
#     return pawn#table[:pom]+"S"+table[pom+1:]

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
    # !!!provera pozicije!!!!!!
    return read_int_from_range_and_prefered("walls", 0, 18, 9)


def read_start_positions(table_columns: int, table_rows: int) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    # tuple[int, int] je pozicija jednog pesaka
    first_player_1 = read_pawn_position(
        "first player first pawn", table_columns, table_rows, 4, 4, [])
    first_player_2 = read_pawn_position(
        "first player second pawn", table_columns, table_rows, 4, 4, [first_player_1])

    second_player_1 = read_pawn_position(
        "second player first pawn", table_columns, table_rows, 4, 4, [first_player_1, first_player_2])
    second_player_2 = read_pawn_position("second player second pawn", table_columns, table_rows, 4, 4, tuple[
                                         first_player_1, first_player_2, second_player_1])

    return [(first_player_1, first_player_2), (second_player_1, second_player_2)]
