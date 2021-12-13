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

    if is_horizontal and ((row,column) in walls_horizontal or (row,column-1) in walls_horizontal or (row,column) in walls_vertical):
        return False

    if not is_horizontal and ((row,column) in walls_vertical or (row-1,column) in walls_vertical or (row,column) in walls_horizontal):
        return False

    return True


def is_player_movement_valid(
    walls_vertical: list[str],
    walls_horizontal: list[str],
    pawn1:tuple[int,int],
    pawn2:tuple[int,int],
    table_rows: int,
    table_columns: int,
    row_old: int,
    column_old: int,
    row_new: int,
    column_new: int,
    )->bool:
    if column_new<0 or row_new<0 or column_new>table_columns or row_new>table_rows or (row_old==row_new and column_old==column_new):
        return False
    
    if row_old-2==row_new:
        if (row_old-1,column_old) in walls_horizontal:
            print
    elif row_old+2==row_new:
        print 
    elif column_old-2==column_new:
        print
    elif column_old+2==column_new:
        print
    elif row_old-1==row_new:
        if column_old-1==column_new:
            print
        else:
            print
    elif row_old+1==row_new:
        if column_old-1==column_new:
            print
        else:
            print
    return


def move_player(
    walls_vertical: list[str],
    walls_horizontal: list[str],
    pawn1:tuple[int,int],
    pawn2:tuple[int,int],
    table_rows: int,
    table_columns: int,
    row_old: int,
    column_old: int,
    row_new: int,
    column_new: int,
    )->bool:
    if not is_player_movement_valid(walls_vertical,walls_horizontal,pawn1,pawn2,table_rows, table_columns, row_old, column_old, row_new, column_new):
        return False
    
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
    if(not is_wall_place_valid(walls_vertical, walls_horizontal, table_rows, table_columns, row, column, is_horizontal)):
        return False
    if is_horizontal:
        walls_horizontal.append((row,column))
    else:
        walls_vertical.append((row,column))

    update_heat_map(heat_map, table_rows, table_columns, row, column)

    return


def update_heat_map(heat_map: dict[str, int],table_rows: int, table_columns: int, row: int, column: int) -> None:
    position =(row,column)
    heat_map[position]+=1
    #dopuniti!!!!!!!!!!!!
    return
