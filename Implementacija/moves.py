from utility import int_to_table_coordinate

def is_game_end(
    pawn_x1: tuple[int, int],
    pawn_x2: tuple[int, int],
    pawn_o1: tuple[int, int],
    pawn_o2: tuple[int, int],
    start_positions_x: list[tuple[int, int]],
    start_positions_o: list[tuple[int, int]]
) -> int:

    if pawn_o1 in start_positions_x or pawn_o2 in start_positions_x:
        return 1
    if pawn_x1 in start_positions_o or pawn_x2 in start_positions_o:
        return 2
    return 0


def is_player_movement_valid(state: dict[str, tuple[int, int]], old_row: int, old_column: int, new_row: int, new_column: int):
    # if(state[])
    return


def is_wall_place_valid(
    walls_vertical: list[str],
    walls_horizontal: list[str],
    table_rows: int,
    table_columns: int,
    row: int,
    column: int,
    is_horizontal: bool
) -> bool:
    if table_rows == row or table_columns == column:
        return False

    position = int_to_table_coordinate(row)+int_to_table_coordinate(column)
    position_next = int_to_table_coordinate(#left
        row)+int_to_table_coordinate(column-1) if column!=0 else ""

    if is_horizontal and (position in walls_horizontal or position_next in walls_horizontal or position in walls_vertical):
        return False

    position_next = int_to_table_coordinate(#up position
        row-1)+int_to_table_coordinate(column) if column!=0 else ""  
    if not is_horizontal and (position in walls_vertical or position_next in walls_vertical or position in walls_horizontal):
        return False
    
    
    return True


def move_player():
    return


def place_wall(
    walls_vertical: list[str],
    walls_horizontal: list[str],
    heat_map: dict[str, int],
    table_rows: int,
    table_columns: int,
    row: int,
    column: int,
    is_horizontal: bool
) -> bool:
    if(not is_wall_place_valid(walls_vertical, walls_horizontal, table_rows, table_columns, row, column,is_horizontal)):
        return False
    position = int_to_table_coordinate(row)+int_to_table_coordinate(column)

    if is_horizontal:
        walls_horizontal.append(position)
    else:
        walls_vertical.append(position)
    
    update_heat_map(heat_map,row,column)

    return


def update_heat_map(heat_map:dict[str, int], row: int, column: int) -> None:
    
    return
