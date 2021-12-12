def is_game_end(#to change
    pawn_x1: tuple[int, int],
    pawn_x2: tuple[int, int],
    pawn_o1: tuple[int, int],
    pawn_o2: tuple[int, int],
    start_positions_x:list[tuple[int,int]],
    start_positions_o:list[tuple[int,int]]
) -> bool:
    if pawn_o1 in start_positions_x or pawn_o2 in start_positions_x:
        print("O player is winner!")
        return True
    if pawn_x1 in start_positions_o or pawn_x2 in start_positions_o:
        print("X player is winner!")
        return True
    return False


def is_player_movement_valid(state:dict[str,tuple[int,int,int]],old_i:int,old_j,new_i:int,new_j):
    #if(state[])
    return


def is_wall_place_valid():
    return


def move_player():
    return


def place_wall():
    return
