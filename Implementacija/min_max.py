from moves import is_pawn_move_valid, is_wall_place_valid, place_wall
from path_finding import generate_next_moves
from utility import add_to_tuple, add_wall_in_tuple, decrement_number_of_walls, update_pawn_positions


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
    if depth==0:
        return (current_pawns_positions,start_positions,walls,table_size,heat_map)
    
    for state in next_states():
        pass

    

def next_states(#nije testirano!!!!!!!!!!!!!!!!
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int,int],...], tuple[tuple[int,int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    selected_player_index: int,
    heat_map: dict[tuple[int, int], int],
    ):#list novih stanja
    state=[]
    all_walls=generate_walls_positions(walls,number_of_walls,table_size,selected_player_index)
    all_pawn_positions=generate_pawns_positions(current_pawns_positions,start_positions,walls,table_size,selected_player_index)
    
    new_number_of_walls=decrement_number_of_walls(number_of_walls,selected_player_index,False)
    for new_pawn in all_pawn_positions[0]:
        new_pawns_positions=update_pawn_positions(current_pawns_positions,selected_player_index,0,new_pawn)
        for new_wall in all_walls[0]:
            # if is_wall_place_valid(walls,table_size,new_wall,False): #ne pozivam jer moguc update za params
            new_walls=add_wall_in_tuple(walls,new_wall,0)
            state.append((new_pawns_positions,start_positions,new_walls,new_number_of_walls,table_size,not selected_player_index,heat_map))


    new_number_of_walls=decrement_number_of_walls(number_of_walls,selected_player_index,True)
    for new_pawn in all_pawn_positions[1]:
        new_pawns_positions=update_pawn_positions(current_pawns_positions,selected_player_index,1,new_pawn)
        for new_wall in all_walls[1]:    
            new_walls=add_wall_in_tuple(walls,new_wall,1)
            state.append((new_pawns_positions,start_positions,new_walls,new_number_of_walls,table_size,not selected_player_index,heat_map))
    
    return state


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


def generate_walls_positions(
    walls: tuple[tuple, tuple],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    selected_player_index: int,
    )->tuple[list[tuple[int,int]],list[tuple[int,int]]]:
    new_walls=([],[])
    if number_of_walls[selected_player_index][0] >0:
        for i in range(1,table_size[0]):
            for j in range(1,table_size[1]+1):
                if (i,j) not in walls[0] and is_wall_place_valid(walls,table_size,(i,j),0):
                    new_walls[0].append((i,j))

    if number_of_walls[selected_player_index][1] >0:
        for i in range(1,table_size[0]+1):
            for j in range(1,table_size[1]):
                  if (i,j) not in walls[1] and is_wall_place_valid(walls,table_size,(i,j),1):
                    new_walls[1].append((i,j))

    return new_walls

def generate_pawns_positions(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int
    )->tuple[list[tuple[int,int]],list[tuple[int,int]]]:
   return (generate_next_moves(current_pawns_positions,start_positions,walls,table_size,selected_player_index,0,current_pawns_positions[selected_player_index][0]),
    generate_next_moves(current_pawns_positions,start_positions,walls,table_size,selected_player_index,1,current_pawns_positions[selected_player_index][1]))
