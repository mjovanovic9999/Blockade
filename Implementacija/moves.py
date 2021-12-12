def is_game_end(#to change
    pawn_x1: tuple[int, int],
    pawn_x2: tuple[int, int],
    pawn_o1: tuple[int, int],
    pawn_o2: tuple[int, int],
    start_positions_x:list[tuple[int,int]],
    start_positions_o:list[tuple[int,int]]
    ) -> int:

    if pawn_o1 in start_positions_x or pawn_o2 in start_positions_x:
        return 1
    if pawn_x1 in start_positions_o or pawn_x2 in start_positions_o:
        return 2
    return 0


def is_player_movement_valid(state:dict[str,tuple[int,int,int]],old_row:int,old_column:int,new_row:int,new_column:int):
    #if(state[])
    return


def is_wall_place_valid(
    state:dict[str,tuple[int,int,int]],
    table_rows: int,
    table_columns: int,

    i:int,
    j:int,
    )->bool:
    if table_rows==i or table_columns==j:
        return False

    return True


def move_player():
    return


def place_wall(
    state:dict[str,tuple[int,int,int]],
    table_rows: int,
    table_columns: int,
    i:int,
    j:int,
    is_horizontal:bool
    )->bool:
    if(not is_wall_place_valid(state, table_rows,table_columns, i,j)):
        return False
    print("C")
    if is_horizontal and state("ced")[1]==1:
        return False
#tuuuuuuuuuuuuuuuuuuuuuuuuuuuuu

    return
