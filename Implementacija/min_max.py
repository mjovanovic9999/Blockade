import os
import threading
import time
from os import stat
from moves import is_pawn_move_valid_with_indexes, is_wall_place_valid
from path_finding import generate_next_moves
from utility import add_wall_in_tuple, decrement_number_of_walls, remove_wall_from_tuple, update_pawn_positions, update_tuple, update_tuple_many


# current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
# walls: tuple[tuple, tuple],
# number_of_walls: tuple[tuple[int, int], tuple[int, int]],
# heat_map: dict[tuple[int, int], int],
#

def min_max(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth: int,
    is_player_min: bool,
    alpha: int,
    beta: int,
):
    generate_vertical = number_of_walls[0][0] > 0 or number_of_walls[1][0] > 0
    generate_horizontal = number_of_walls[0][1] > 0 or number_of_walls[1][1] > 0

    previous_generated_walls = generate_walls_positions(walls, table_size, generate_vertical, generate_horizontal)
    start_time=time.time()
    pom= min_value(current_pawns_positions, start_positions, walls, number_of_walls, table_size, heat_map, depth, is_player_min, alpha, beta, previous_generated_walls, None, None, None)\
        if is_player_min else \
        max_value(current_pawns_positions, start_positions, walls, number_of_walls,
                  table_size, heat_map, depth, is_player_min, alpha, beta, previous_generated_walls, None, None, None)
    print("near su "+str(near[0])+" far su "+str(far[0])+" za vreme "+str(time.time()-start_time)+" procenti "+(str(near[0]/(near[0]+far[0  ]))))
    input()  
 
    return pom


def next_states(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    is_player_min: bool,  # isto kao selected index
    heat_map: dict[tuple[int, int], int],
    previous_generated_walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
):  # list novih stanja
    state = []
    all_pawn_positions = generate_less_pawn_positions( current_pawns_positions, start_positions, walls, table_size, is_player_min)

    #if threading.get_ident() not in mrs_stanje_dict.keys():
        #mrs_stanje_dict[threading.get_ident()]=0
        

    new_number_of_walls = decrement_number_of_walls(
        number_of_walls, is_player_min, False)
    for new_pawn in all_pawn_positions[0]:
        new_pawns_positions = update_pawn_positions(current_pawns_positions, is_player_min, 0, new_pawn)
        if previous_generated_walls != ((), ()):
            for new_wall in previous_generated_walls[0]:
                #mrs_stanje_dict[threading.get_ident()]+=1
                if is_state_good(new_pawns_positions,start_positions,new_wall,is_player_min):
                # if is_wall_place_valid(walls,table_size,new_wall,False): #ne pozivam jer moguc update za params!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    new_walls = add_wall_in_tuple(walls, new_wall, 1)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                new_number_of_walls, table_size, not is_player_min, heat_map))
                    near[0]+=1
                else:
                        far[0]+=1
            for new_wall in previous_generated_walls[1]:
                #mrs_stanje_dict[threading.get_ident()]+=1

                if is_state_good(new_pawns_positions,start_positions,new_wall,is_player_min):
                # if is_wall_place_valid(walls,table_size,new_wall,False): #ne pozivam jer moguc update za params!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    new_walls = add_wall_in_tuple(walls, new_wall, 0)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                new_number_of_walls, table_size, not is_player_min, heat_map))
                    near[0]+=1
                else:
                    far[0]+=1
        else:
           # mrs_stanje_dict[threading.get_ident()]+=1
            state.append((new_pawns_positions, start_positions, walls,
                          number_of_walls, table_size, not is_player_min, heat_map))

    new_number_of_walls = decrement_number_of_walls(
        number_of_walls, is_player_min, True)
    for new_pawn in all_pawn_positions[1]:
        new_pawns_positions = update_pawn_positions(
            current_pawns_positions, is_player_min, 1, new_pawn)
        if previous_generated_walls != ((), ()):
            for new_wall in previous_generated_walls[0]:
                # mrs_stanje_dict[threading.get_ident()]+=1
                if is_state_good(new_pawns_positions,start_positions,new_wall,is_player_min):
                    new_walls = add_wall_in_tuple(walls, new_wall, 0)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                new_number_of_walls, table_size, not is_player_min, heat_map))
                    near[0]+=1
                else:
                    far[0]+=1
            for new_wall in previous_generated_walls[1]:
                # mrs_stanje_dict[threading.get_ident()]+=1
                if is_state_good(new_pawns_positions,start_positions,new_wall,is_player_min):
                    new_walls = add_wall_in_tuple(walls, new_wall, 1)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                new_number_of_walls, table_size, not is_player_min, heat_map))
                    near[0]+=1
                else:
                    far[0]+=1

        else:
            # mrs_stanje_dict[threading.get_ident()]+=1
        
            state.append((new_pawns_positions, start_positions, walls,
                          number_of_walls, table_size, not is_player_min, heat_map))
    return state                

def is_state_good(
    new_pawns_positions:tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions:tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    new_wall:tuple[int, int],
    is_player_min:bool
)->bool:
    dest_column=start_positions[not is_player_min][0][1]
    for pawn in new_pawns_positions[is_player_min]:#mozda bez celo ovo jer evaluate ga nema odabere ili da se smanji
        temp=(new_wall[0]-pawn[0],new_wall[1]-pawn[1])
        if pawn[1]<dest_column:#ide na desno #mozda da se smanji zbog bliski susret
            if temp in [
            (-3,1),
            (-2,0),(-2,1),(-2,2),
            (-1,0),(-1,1),(-1,2),#bilo je i -2,3
            (0,0),(0,1),(0,2),(0,3),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2),
            (3,1)
            ]:
                return False
        elif pawn[1]>dest_column:#ide na levo
            if temp in [
            (-3,-2),
            (-2,-1),(-2,-2),(-2,-3),
            (-1,-1),(-1,-2),(-1,-3),
            (0,-1),(0,-2),(0,-3),(0,-4),
            (1,-1),(1,-2),(1,-3),
            (2,-1),(2,-2),(2,-3),
            (3,-2)
            ]:
                return False 

        #da se orgadi kuca
    if  is_near(start_positions[is_player_min][0],new_wall,1) or is_near(start_positions[is_player_min][1],new_wall,1) :
        # new_wall is in  (-2,-2),(-2,2)...
        return True

    start_column=start_positions[is_player_min][0][1]
    for enemy_pawn in new_pawns_positions[not is_player_min]:
        temp=(new_wall[0]-enemy_pawn[0],new_wall[1]-enemy_pawn[1])
        if enemy_pawn[1]<start_column:
            if temp in [
            (-1,0),#(-1,1),
            (0,0),#(0,1),#(0,2),
            (-1,0),#(-1,1),
            ]:#moze i dodatno samo: (-2,2),(2,2) 
                return True
        elif enemy_pawn[1]>start_column:
            if temp in [
            (-1,-1),#(-1,-1),
            (0,-1),#(0,-2),#(0,-2),
            (-1,-1),#(-1,-1),
            ]:
                return True
        else:
            True
    
    return False

    
# mrs_stanje_dict={-1:-1}
near=[0]
far=[0]

rez_array = []
previous_pawns=[]
threads = []
# count = dict()
start_depth=5


def is_near(position1:tuple[int, int],position2:tuple[int, int],distance:int)->bool:
    if abs(position1[0]-position2[0])<=distance and abs(position1[1]-position2[1])<=distance:
        #near[0]+=1
        # print("near"+str(near[0]))
        return True
    #far[0]+=1
    # print("far"+str(far[0]))
    return False
    # return True

def evaluate_wall(new_pawns_positions:tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions:tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    new_wall:tuple[int, int])->int:
    pass

def distance(next_pos: tuple[int, int], dest_pos: tuple[int, int]) -> int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])



def evaluate_state(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int]  # jos neki param za sl fazu
) -> int:  # koliko smo blizu pobede
    max = distance(current_pawns_positions[0][0], start_positions[1][0]) +\
        distance(current_pawns_positions[0][0], start_positions[1][1]) +\
        distance(current_pawns_positions[0][1], start_positions[1][0]) +\
        distance(current_pawns_positions[0][1], start_positions[1][1])

    min = distance(current_pawns_positions[1][0], start_positions[0][0]) +\
        distance(current_pawns_positions[1][0], start_positions[0][1]) +\
        distance(current_pawns_positions[1][1], start_positions[0][0]) +\
        distance(current_pawns_positions[1][1], start_positions[0][1])

    result = min-max
    if current_pawns_positions[0][0] == start_positions[1][0] or current_pawns_positions[0][0] == start_positions[1][1] or\
            current_pawns_positions[0][1] == start_positions[1][0] or current_pawns_positions[0][1] == start_positions[1][1]:
        result += 2

    if current_pawns_positions[1][0] == start_positions[0][0] or current_pawns_positions[1][0] == start_positions[0][1] or\
            current_pawns_positions[1][1] == start_positions[0][0] or current_pawns_positions[1][1] == start_positions[0][1]:
        result -= 2
    return result
# current_pawns_positions,start_positions,walls,number_of_walls,table_size,heat_map,depth,is_player_min,alpha,beta




def max_value(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth: int,
    is_player_min: bool,
    alpha: int,
    beta: int,
    previous_generated_walls: tuple[tuple[tuple[int,
                                                int], ...], tuple[tuple[int, int], ...]] = None,
    state_current_pawns_positions: tuple[tuple[tuple[int, int],
                                               tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]] = None,
    state_walls: tuple[tuple[tuple[int, int], ...],
                       tuple[tuple[int, int], ...]] = None,
    state_number_of_walls: tuple[tuple[int, int], tuple[int, int]] = None
):
    if depth == 0:
        return (
            current_pawns_positions,
            start_positions,
            walls,
            number_of_walls,
            table_size,
            heat_map,
            depth,
            is_player_min,
            alpha,
            beta,
            state_current_pawns_positions,
            state_walls,
            state_number_of_walls,
            evaluate_state(current_pawns_positions, start_positions,
                           walls, number_of_walls, table_size, heat_map)
        )
    beta = (current_pawns_positions,
            start_positions,
            walls,
            number_of_walls,
            table_size,
            heat_map,
            depth,
            is_player_min,
            alpha,
            beta,
            state_current_pawns_positions,
            state_walls,
            state_number_of_walls,
            beta)  # 0 je placeholder
    alpha = (current_pawns_positions,
             start_positions,
             walls,
             number_of_walls,
             table_size,
             heat_map,
             depth,
             is_player_min,
             alpha,
             beta[-1],
             state_current_pawns_positions,
             state_walls,
             state_number_of_walls,
             alpha)

    for (
        new_current_pawns_positions,
        new_start_positions,
        new_walls,
        new_number_of_walls,
        new_table_size,
        new_is_player_min,
        new_heat_map
    ) in next_states(
        current_pawns_positions,
        start_positions,
        walls,
        number_of_walls,
        table_size,
        is_player_min,
        heat_map,
        previous_generated_walls
    ):

        def max_thread():
            rez = max_value(new_current_pawns_positions, new_start_positions,   new_walls,  new_number_of_walls,
                            new_table_size, new_heat_map,  depth -
                            1,  new_is_player_min,  alpha[-1],   beta[-1],   previous_generated_walls,
                            new_current_pawns_positions if state_current_pawns_positions is None else state_current_pawns_positions,
                            new_walls if state_walls is None else state_walls,
                            new_number_of_walls if state_number_of_walls is None else state_number_of_walls)
            rez_array.append(rez)

        if depth == start_depth:# and new_current_pawns_positions not in previous_pawns:
            previous_pawns.append(new_current_pawns_positions)
            threads.append(threading.Thread(target=max_thread))
            # count[0] = count[0]+1
            threads[-1].start()

        if depth != start_depth:
            alpha = max(alpha, max_value(new_current_pawns_positions,
                                         new_start_positions,
                                         new_walls,
                                         new_number_of_walls,
                                         new_table_size,
                                         new_heat_map,
                                         depth-1,
                                         new_is_player_min,
                                         alpha[-1],
                                         beta[-1],
                                         previous_generated_walls,
                                         new_current_pawns_positions if state_current_pawns_positions is None else state_current_pawns_positions,
                                         new_walls if state_walls is None else state_walls,
                                         new_number_of_walls if state_number_of_walls is None else state_number_of_walls
                                         ),
                        key=lambda x: x[-1]
                        )
        if alpha[-1] >= beta[-1]:
            return beta
    if depth == start_depth:
        for th in threads:
            th.join()

        return max(rez_array, key=lambda x: x[-1])
    return alpha


def min_value(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    depth: int,
    is_player_min: bool,
    alpha: int,
    beta: int,
    previous_generated_walls: tuple[tuple[tuple[int,  int], ...], tuple[tuple[int, int], ...]],
    state_current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]] = None,
    state_walls: tuple[tuple[tuple[int, int], ...],tuple[tuple[int, int], ...]] = None,
    state_number_of_walls: tuple[tuple[int, int], tuple[int, int]] = None
):
    if depth == 0:
        return (
            current_pawns_positions,
            start_positions,
            walls,
            number_of_walls,
            table_size,
            heat_map,
            depth,
            is_player_min,
            alpha,
            beta,
            state_current_pawns_positions,
            state_walls,
            state_number_of_walls,
            evaluate_state(current_pawns_positions, start_positions,
                           walls, number_of_walls, table_size, heat_map)
        )
    beta = (current_pawns_positions,
            start_positions,
            walls,
            number_of_walls,
            table_size,
            heat_map,
            depth,
            is_player_min,
            alpha,
            beta,
            state_walls,
            state_number_of_walls,
            beta)  # 0 je placeholder
    alpha = (current_pawns_positions,
             start_positions,
             walls,
             number_of_walls,
             table_size,
             heat_map,
             depth,
             is_player_min,
             alpha,
             beta[-1],
             state_walls,
             state_number_of_walls,
             alpha)

    for (
        new_current_pawns_positions,
        new_start_positions,
        new_walls,
        new_number_of_walls,
        new_table_size,
        new_is_player_min,
        new_heat_map
    ) in next_states(
        current_pawns_positions,
        start_positions,
        walls,
        number_of_walls,
        table_size,
        is_player_min,
        heat_map,
        previous_generated_walls
    ):
        beta = min(beta, max_value(new_current_pawns_positions,
                                   new_start_positions,
                                   new_walls,
                                   new_number_of_walls,
                                   new_table_size,
                                   new_heat_map,
                                   depth-1,
                                   new_is_player_min,
                                   alpha[-1],
                                   beta[-1],
                                   previous_generated_walls,
                                   new_current_pawns_positions if state_current_pawns_positions is None else state_current_pawns_positions,
                                   new_walls if state_walls is None else state_walls,
                                   new_number_of_walls if state_number_of_walls is None else state_number_of_walls
                                   ),
                   key=lambda x: x[-1]
                   )
        if alpha[-1] >= beta[-1]:
            return alpha
    return beta


def generate_walls_positions(
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    generate_vertical: bool,
    generate_horizontal: bool,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    vertical_walls = []
    if generate_vertical:
        for i in range(1, table_size[0]):
            for j in range(1, table_size[1]+1):
                if (i, j) not in walls[0] and is_wall_place_valid(walls, table_size, (i, j), 0):
                    vertical_walls.append((i, j))

    horizontal_walls = []
    if generate_horizontal:
        for i in range(1, table_size[0]+1):
            for j in range(1, table_size[1]):
                if (i, j) not in walls[1] and is_wall_place_valid(walls, table_size, (i, j), 1):
                    horizontal_walls.append((i, j))

    return (tuple(vertical_walls), tuple(horizontal_walls))


def generate_pawns_positions(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    selected_player_index: int
) -> list[list[tuple[int, int]], list[tuple[int, int]]]:
    return [generate_next_moves(current_pawns_positions, start_positions, walls, table_size, selected_player_index, 0, current_pawns_positions[selected_player_index][0]),
            generate_next_moves(current_pawns_positions, start_positions, walls, table_size, selected_player_index, 1, current_pawns_positions[selected_player_index][1])]


def generate_less_pawn_positions( 
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    is_player_min: int
    )->tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    all_pawn_positions = generate_pawns_positions( current_pawns_positions, start_positions, walls, table_size, is_player_min)
    dest_column=start_positions[not is_player_min][0][1]
    
    pawn_colum=current_pawns_positions[is_player_min][0][1]
    if len(all_pawn_positions[0])>5:
        if pawn_colum<dest_column:#ide ka desno
            all_pawn_positions[0]=list(filter(lambda x: x[1]>pawn_colum,all_pawn_positions[0]))#mozda >=
        elif pawn_colum>dest_column:#ide ka levo
            all_pawn_positions[0]=list(filter(lambda x: x[1]<pawn_colum,all_pawn_positions[0]))
    
    pawn_colum=current_pawns_positions[is_player_min][1][1]
    if len(all_pawn_positions[1])>5:
        if pawn_colum<dest_column:#ide ka desno
            all_pawn_positions[1]=list(filter(lambda x: x[1]>pawn_colum,all_pawn_positions[1]))
        elif pawn_colum>dest_column:#ide ka levo
            all_pawn_positions[1]=list(filter(lambda x: x[1]<pawn_colum,all_pawn_positions[1]))
    
    return tuple(all_pawn_positions)