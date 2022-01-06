from moves import is_pawn_move_valid, is_wall_place_valid
from path_finding import generate_next_moves
from utility import  add_wall_in_tuple, decrement_number_of_walls, update_pawn_positions


def min_max(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth:int,
    is_player_min:bool,
    alpha:int,
    beta:int
    ):
    #vraca potez #depth se smanjuje #kao da smo mi max player #alpha je +beskonacno
    
    # new_states= next_states()#nema params
    # funct=max_state if not is_player_min else min_state #mozda drugacije al neka ga za sad

    # if depth==0 or new_states is None:
    #     return (current_pawns_positions,start_positions,walls,table_size,heat_map,evaluate_state())#fale params

    #                     #x je stanje
    # return funct([min_max(x,depth-1,not is_player_min) for x in new_states])
    
    return min_value(current_pawns_positions,start_positions,walls,table_size,heat_map,depth,is_player_min,alpha,beta)\
            if is_player_min else \
            max_value(current_pawns_positions,start_positions,walls,table_size,heat_map,depth,is_player_min,alpha,beta)    

def next_states(#nije testirano!!!!!!!!!!!!!!!!
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int,int],...], tuple[tuple[int,int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    is_player_min: bool,#isto kao selected index
    heat_map: dict[tuple[int, int], int],
    ):#list novih stanja
    state=[]
    all_walls=generate_walls_positions(walls,number_of_walls,table_size,is_player_min)
    all_pawn_positions=generate_pawns_positions(current_pawns_positions,start_positions,walls,table_size,is_player_min)
    
    new_number_of_walls=decrement_number_of_walls(number_of_walls,is_player_min,False)
    for new_pawn in all_pawn_positions[0]:
        new_pawns_positions=update_pawn_positions(current_pawns_positions,is_player_min,0,new_pawn)
        for new_wall in all_walls[0]:
            # if is_wall_place_valid(walls,table_size,new_wall,False): #ne pozivam jer moguc update za params!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            new_walls=add_wall_in_tuple(walls,new_wall,0)
            state.append((new_pawns_positions,start_positions,new_walls,new_number_of_walls,table_size,not is_player_min,heat_map))

    new_number_of_walls=decrement_number_of_walls(number_of_walls,is_player_min,True)
    for new_pawn in all_pawn_positions[1]:
        new_pawns_positions=update_pawn_positions(current_pawns_positions,is_player_min,1,new_pawn)
        for new_wall in all_walls[1]:    
            new_walls=add_wall_in_tuple(walls,new_wall,1)
            state.append((new_pawns_positions,start_positions,new_walls,new_number_of_walls,table_size,not is_player_min,heat_map))
    
    return state


def distance(next_pos: tuple[int, int], dest_pos: tuple[int, int])->int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])

def evaluate_state(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int]#jos neki param za sl fazu
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

def max_value(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth:int,
    is_player_min:bool,
    alpha:int,
    beta:int
    )->int:
    if depth==0:
        return (
        current_pawns_positions,
        start_positions,
        walls,
        table_size,
        heat_map,
        evaluate_state(current_pawns_positions, start_positions,walls,table_size,heat_map)
        )
    beta=(0,beta)#0 je placeholder
    alpha=(0,alpha)
    for (a,b,c,d,e,f,g) in next_states(
        current_pawns_positions,
        start_positions,
        walls,
        table_size,
        heat_map,
        is_player_min,
        heat_map,
        ):
        alpha=max(alpha,
            min_value(a,b,c,d,e,f,g,depth-1,alpha[-1],beta[-1]),
            key=lambda x: x[-1]
        )
        if alpha[-1]>=beta[-1]:
            return beta
    return alpha


def min_value(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth:int,
    is_player_min:bool,
    alpha:int,
    beta:int
    )->int:
    if depth==0:
        return (
        current_pawns_positions,
        start_positions,
        walls,
        table_size,
        heat_map,
        evaluate_state(current_pawns_positions, start_positions,walls,table_size,heat_map)
        )
    beta=(0,beta)#0 je placeholder
    alpha=(0,alpha)
    for (a,b,c,d,e,f,g) in next_states(
        current_pawns_positions,
        start_positions,
        walls,
        table_size,
        heat_map,
        is_player_min,
        heat_map,
        ):
        beta=min(beta,
            max_value(a,b,c,d,e,f,g,depth-1,alpha[-1],beta[-1]),
            key=lambda x: x[-1]
        )
        if alpha[-1]>=beta[-1]:
            return beta
    return alpha


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
