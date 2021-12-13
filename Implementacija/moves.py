from utility import int_to_table_coordinate


def is_game_end(
    pawn_x1: tuple[int, int],
    pawn_x2: tuple[int, int],
    pawn_o1: tuple[int, int],
    pawn_o2: tuple[int, int],
    start_positions_x: list[tuple[int, int]],
    start_positions_o: list[tuple[int, int]]
) -> bool:

    return pawn_x1 in start_positions_o or pawn_x2 in start_positions_o or pawn_o1 in start_positions_x or pawn_o2 in start_positions_x
        


def is_wall_place_valid(
    walls_vertical: list[tuple[int,int]],
    walls_horizontal: list[tuple[int,int]],
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
    walls_vertical: list[tuple[int,int]],
    walls_horizontal: list[tuple[int,int]],
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
        if (row_old-1,column_old) in walls_horizontal or (row_old-1,column_old-1) in walls_horizontal or  (row_old-2,column_old) in walls_horizontal or (row_old-2,column_old-1) in walls_horizontal:
            return False
    elif row_old+2==row_new:
        if (row_old,column_old) in walls_horizontal or (row_old,column_old-1) in walls_horizontal or  (row_old+1,column_old) in walls_horizontal or (row_old+1,column_old-1) in walls_horizontal:
            return False
    elif column_old-2==column_new:
        if (row_old,column_old-1) in walls_vertical or (row_old-1,column_old-1) in walls_vertical or  (row_old,column_old-2) in walls_vertical or (row_old-1,column_old-2) in walls_vertical:
            return False
    elif column_old+2==column_new:
        if (row_old,column_old) in walls_vertical or (row_old-1,column_old) in walls_vertical or  (row_old,column_old+1) in walls_vertical or (row_old-1,column_old+1) in walls_vertical:
            return False
    elif row_old-1==row_new:
        if column_old-1==column_new:
            if\
                ((row_old,column_old-1) in walls_vertical and (row_old-1,column_old) in walls_horizontal)or \
                ((row_old,column_old-1) in walls_vertical and (row_old-1,column_old-1) in walls_horizontal)or \
                ((row_old-1,column_old-1) in walls_vertical and (row_old-1,column_old) in walls_horizontal) :
                return False
        elif\
                ((row_old,column_old) in walls_vertical and (row_old-1,column_old-1) in walls_horizontal)or \
                ((row_old,column_old) in walls_vertical and (row_old-1,column_old) in walls_horizontal)or \
                ((row_old-1,column_old) in walls_vertical and (row_old-1,column_old-1) in walls_horizontal) :
                return False
    elif row_old+1==row_new:
        if column_old-1==column_new:
            if\
                ((row_old,column_old-1) in walls_vertical and (row_old,column_old) in walls_horizontal)or \
                ((row_old,column_old-1) in walls_vertical and (row_old,column_old-1) in walls_horizontal)or \
                ((row_old-1,column_old-1) in walls_vertical and (row_old,column_old) in walls_horizontal) :
                return False
        else:
            if\
                ((row_old-1,column_old) in walls_vertical and (row_old,column_old-1) in walls_horizontal)or \
                ((row_old,column_old) in walls_vertical and (row_old,column_old-1) in walls_horizontal)or \
                ((row_old-1,column_old) in walls_vertical and (row_old,column_old) in walls_horizontal) :
                return False


    return True

def position_occupied(
    pawn1:tuple[int,int],
    pawn2:tuple[int,int],
    row_old: int,
    column_old: int,
    row_new: int,
    column_new: int,
    )->tuple[int,int]:

    if row_old-2==row_new:
        return (row_new+1,column_new)
    elif row_old+2==row_new:
        return (row_new-1,column_new)
    elif column_old-2==column_new:
        return (row_new,column_new+1)
    elif column_old+2==column_new:
        return (row_new,column_new-1)
    return(row_old,column_new)
    # elif row_old-1==row_new:
    #     if column_old-1==column_new:
    #         print
    #     else:
    #         print
    # elif row_old+1==row_new:
    #     if column_old-1==column_new:
    #         print
    #     else:
    #         print
    #da opet unese poziciju ako je dijagonala zauzeta

    return

def move_player(
    walls_vertical: list[tuple[int,int]],
    walls_horizontal: list[tuple[int,int]],
    my_pawn:tuple[int,int],
    pawn1:tuple[int,int],
    pawn2:tuple[int,int],
    table_rows: int,
    table_columns: int,
    row_new: int,
    column_new: int,
    )->tuple[int,int]:
    row_old= my_pawn[0]
    column_old=my_pawn[1]

    if not is_player_movement_valid(walls_vertical,walls_horizontal,table_rows, table_columns, row_old, column_old, row_new, column_new):
        return my_pawn
    if pawn1==(row_new,column_new) or pawn2==(row_new,column_new):
        move=position_occupied(pawn1,pawn2,row_old,column_old,row_new,column_new)
    else:
        move=(row_new,column_new)
    return move

def place_wall(
    walls_vertical: list[tuple[int,int]],
    walls_horizontal: list[tuple[int,int]],
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

    return True


def update_heat_map(heat_map: dict[tuple[int, int], int],table_rows: int, table_columns: int, row: int, column: int) -> None:
    position =(row,column)
    heat_map[position]+=1
    #dopuniti!!!!!!!!!!!!
    return
