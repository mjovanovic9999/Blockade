def min_max(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth:int,
    is_player_max:bool,
    alpha:int,
    beta:int
    ):
    #vraca potez #depth se smanjuje #kao da smo mi max player #alpha je +beskonacno

    pass


def next_states(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int]
    ):#list novih stanja
    pass



def distance(next_pos: tuple[int, int], dest_pos: tuple[int, int])->int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])

def evaluate_state(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int]
)->int:#koliko smo blizu pobede
    max=distance(current_pawns_positions[0][0],start_positions[1][0])+\
    distance(current_pawns_positions[0][0],start_positions[1][1])+\
    distance(current_pawns_positions[0][1],start_positions[1][0])+\
    distance(current_pawns_positions[0][1],start_positions[1][1])

    min=distance(current_pawns_positions[1][0],start_positions[0][0])+\
    distance(current_pawns_positions[1][0],start_positions[0][1])+\
    distance(current_pawns_positions[1][1],start_positions[0][0])+\
    distance(current_pawns_positions[1][1],start_positions[0][1])
    return min-max

def max_state(#best state #isto i za min
    state:list[tuple[tuple,tuple,tuple,tuple,dict]]
    ):
    pass

