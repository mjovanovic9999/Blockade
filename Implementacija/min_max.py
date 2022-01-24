import imp
from frozendict import frozendict
from os import stat
from moves import is_pawn_move_valid_with_indexes, is_wall_place_valid, update_wall_connection_points
from path_finding import a_star, generate_next_moves
from utility import add_wall_in_tuple, decrement_number_of_walls, remove_wall_from_tuple, update_pawn_positions, update_tuple, update_tuple_many


def min_max(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
    depth: int,
    is_player_min: bool,
    alpha: int,
    beta: int,
):
    generate_vertical = number_of_walls[0][0] > 0 or number_of_walls[1][0] > 0
    generate_horizontal = number_of_walls[0][1] > 0 or number_of_walls[1][1] > 0


    dest_pos=start_positions[not is_player_min]


    max_first_temp1=a_star(current_pawns_positions,start_positions,walls,table_size, is_player_min,0,dest_pos[0] ,{})
    max_first_temp2=a_star(current_pawns_positions,start_positions,walls,table_size, is_player_min,0,dest_pos[1] ,{})

    max_first=max_first_temp1 if len(max_first_temp1)<len(max_first_temp2) else max_first_temp2

    max_second_temp1=a_star(current_pawns_positions,start_positions,walls,table_size,is_player_min,1,dest_pos[0] ,{})
    max_second_temp2=a_star(current_pawns_positions,start_positions,walls,table_size,is_player_min,1,dest_pos[1] ,{})

    max_second=max_second_temp1 if len(max_second_temp1)<len(max_second_temp2) else max_second_temp2

    max_paths=(
            max_first,
            max_second
        )


    dest_pos=start_positions[is_player_min]

    min_first_temp1=a_star(current_pawns_positions,start_positions,walls,table_size,not is_player_min,0,dest_pos[0] ,{})
    min_first_temp2=a_star(current_pawns_positions,start_positions,walls,table_size,not is_player_min,0,dest_pos[1] ,{})

    min_first=min_first_temp1 if len(min_first_temp1)<len(min_first_temp2) else min_first_temp2

    min_second_temp1=a_star(current_pawns_positions,start_positions,walls,table_size,not is_player_min,1,dest_pos[0] ,{})
    min_second_temp2=a_star(current_pawns_positions,start_positions,walls,table_size,not is_player_min,1,dest_pos[1] ,{})

    min_second=min_second_temp1 if len(min_second_temp1)<=len(min_second_temp2) else min_second_temp2

    min_paths=(
            min_first,
            min_second
        )
   


    previous_generated_walls = generate_walls_positions(current_pawns_positions, start_positions,
                                                        walls, table_size, connection_points, generate_vertical, generate_horizontal, not is_player_min)
    pom = min_value(current_pawns_positions, start_positions, walls, number_of_walls, table_size, heat_map, connection_points, depth, is_player_min, alpha, beta,(max_paths,min_paths), previous_generated_walls, None, None, None)\
        if is_player_min else \
        max_value(current_pawns_positions, start_positions, walls, number_of_walls,
                  table_size, heat_map, connection_points, depth, is_player_min, alpha, beta,(max_paths,min_paths), previous_generated_walls ,None, None, None)

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
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]]
):  # list novih stanja
    state = []
    all_pawn_positions = generate_less_pawn_positions(
        current_pawns_positions, start_positions, walls, table_size, is_player_min)


    new_number_of_walls = decrement_number_of_walls(
        number_of_walls, is_player_min, False)
    for new_pawn in all_pawn_positions[0]:
        new_pawns_positions = update_pawn_positions(
            current_pawns_positions, is_player_min, 0, new_pawn)
        if previous_generated_walls != ((), ()):
            for new_wall in previous_generated_walls[0]:

                if is_state_good(new_pawns_positions, start_positions, new_wall, is_player_min):
                    if not is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, new_wall, False, connection_points, not is_player_min):
                        continue  

                    new_walls = add_wall_in_tuple(walls, new_wall, 0)
                    connection_points = update_wall_connection_points(connection_points,new_wall, 0)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                  new_number_of_walls, table_size, not is_player_min, heat_map, connection_points))

            for new_wall in previous_generated_walls[1]:

                if is_state_good(new_pawns_positions, start_positions, new_wall, is_player_min):
                    if not is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, new_wall, True, connection_points, not is_player_min):
                        continue
                    new_walls = add_wall_in_tuple(walls, new_wall, 1)
                    connection_points = update_wall_connection_points(connection_points,new_wall, 1)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                  new_number_of_walls, table_size, not is_player_min, heat_map, connection_points))
        else:
            state.append((new_pawns_positions, start_positions, walls,
                         number_of_walls, table_size, not is_player_min, heat_map, connection_points))

    new_number_of_walls = decrement_number_of_walls(
        number_of_walls, is_player_min, True)
    for new_pawn in all_pawn_positions[1]:
        new_pawns_positions = update_pawn_positions(
            current_pawns_positions, is_player_min, 1, new_pawn)
        if previous_generated_walls != ((), ()):
            for new_wall in previous_generated_walls[0]:
                if is_state_good(new_pawns_positions, start_positions, new_wall, is_player_min):
                    if not is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, new_wall, False, connection_points, not is_player_min):
                        continue
                    new_walls = add_wall_in_tuple(walls, new_wall, 0)
                    connection_points = update_wall_connection_points(connection_points,new_wall, 0)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                  new_number_of_walls, table_size, not is_player_min, heat_map, connection_points))

            for new_wall in previous_generated_walls[1]:
                if is_state_good(new_pawns_positions, start_positions, new_wall, is_player_min):
                    if not is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, new_wall, True, connection_points, not is_player_min):
                        continue
                    new_walls = add_wall_in_tuple(walls, new_wall, 1)
                    connection_points = update_wall_connection_points(connection_points,new_wall, 1)
                    state.append((new_pawns_positions, start_positions, new_walls,
                                  new_number_of_walls, table_size, not is_player_min, heat_map, connection_points))
        else:
            state.append((new_pawns_positions, start_positions, walls,
                         number_of_walls, table_size, not is_player_min, heat_map, connection_points))
    return state


def is_state_good(
    new_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    new_wall: tuple[int, int],
    is_player_min: bool
) -> bool:
    dest_column = start_positions[not is_player_min][0][1]
    for pawn in new_pawns_positions[is_player_min]:
        temp = (new_wall[0]-pawn[0], new_wall[1]-pawn[1])
        if pawn[1] < dest_column:  # ide na desno
            if temp in [
                (-3, 1),
                (-2, 0), (-2, 1),# (-2, 2), (-2, 3),  # dodato je i -2,3
                (-1, 0), (-1, 1), (-1, 2),
                (0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (2, 3),
                (2, 0), (2, 1), #(2, 2),
                (3, 1)
            ]:
                return False
        elif pawn[1] > dest_column:  # ide na levo
            if temp in [
                (-3, -2),
                (-2, -1), (-2, -2),# (-2, -3), (-2, -4),
                (-1, -1), (-1, -2), (-1, -3),
                (0, -1), (0, -2), (0, -3), (0, -4),
                (1, -1), (1, -2), (1, -3),
                (2, -1), (2, -2),# (2, -3), (2, -4),
                (3, -2)
            ]:
                return False

    start_column = start_positions[is_player_min][0][1]
    for enemy_pawn in new_pawns_positions[not is_player_min]:
        temp = (new_wall[0]-enemy_pawn[0], new_wall[1]-enemy_pawn[1])
        if enemy_pawn[1] < start_column:
            if temp in [
                (-1, 0),  (-1, 1),
                (0, 0),  (0, 1), #(0, 2),
                (1, 0),  #(1, 1),
            ]:  # moze i dodatno samo: (-2,2),(2,2)
                return True
        elif enemy_pawn[1] > start_column:
            if temp in [
                (-1,-2), (-1,-1),
                #(0,-3), 
                (0, -2), (0, -1),
                (1, -1), #(1, -2)
                # (-1, -0),  (-1, -1),
                # (0, 0),  (0, -1), (0, -2),
                # (-1, -0),  (-1, -1),
            ]:
                return True
        else:
            True

    return False


def distance(next_pos: tuple[int, int], dest_pos: tuple[int, int]) -> int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])


def evaluate_state(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    paths: tuple[tuple[list[tuple[int, int]], list[tuple[int, int]]], tuple[list[tuple[int, int]], list[tuple[int, int]]]],

    heat_map: dict[tuple[int, int], int]
) -> int:
    max = distance(current_pawns_positions[0][0], start_positions[1][0]) +\
        distance(current_pawns_positions[0][0], start_positions[1][1]) +\
        distance(current_pawns_positions[0][1], start_positions[1][0]) +\
        distance(current_pawns_positions[0][1], start_positions[1][1])

    min = distance(current_pawns_positions[1][0], start_positions[0][0]) +\
        distance(current_pawns_positions[1][0], start_positions[0][1]) +\
        distance(current_pawns_positions[1][1], start_positions[0][0]) +\
        distance(current_pawns_positions[1][1], start_positions[0][1])

    result = min-max #jer je manja vrenost bolja



    result *= 2#mozda za 6

    # for min in current_pawns_positions[1]:
    #     for walls_in_type in walls:
    #         for wall in walls_in_type:
    #             result -= distance(wall, min)*2

    # for max in current_pawns_positions[0]:
    #     for walls_in_type in walls:
    #         for wall in walls_in_type:
    #             result += distance(wall, max)*2

    for max in start_positions[0]:
        for walls_in_type in walls:
            for wall in walls_in_type:
                result -= distance(wall, max)*2

    for min in start_positions[1]:
        for walls_in_type in walls:
            for wall in walls_in_type:
                result += distance(wall, min)*2




    max_paths=paths[0]
    if current_pawns_positions[0][0] in max_paths[0]:
        result+=200
    if current_pawns_positions[0][1] in max_paths[1]:
        result+=200


    min_paths=paths[1]
    if current_pawns_positions[1][0] in min_paths[0]:
        result-=200
    if current_pawns_positions[1][1] in min_paths[1]:
        result-=200

    return result


def max_value(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
    depth: int,
    is_player_min: bool,
    alpha: int,
    beta: int,
    paths: tuple[tuple[list[tuple[int, int]], list[tuple[int, int]]], tuple[list[tuple[int, int]], list[tuple[int, int]]]],
    previous_generated_walls: tuple[tuple[tuple[int,
                                                int], ...], tuple[tuple[int, int], ...]],
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
            connection_points,
            depth,
            is_player_min,
            alpha,
            beta,
            state_current_pawns_positions,
            state_walls,
            state_number_of_walls,
            evaluate_state(current_pawns_positions, start_positions,
                           walls, number_of_walls, table_size,paths, heat_map)
        )
    beta = (current_pawns_positions,
            start_positions,
            walls,
            number_of_walls,
            table_size,
            heat_map,
            connection_points,
            depth,
            is_player_min,
            alpha,
            beta,
            state_current_pawns_positions,
            state_walls,
            state_number_of_walls,
            beta)
    alpha = (current_pawns_positions,
             start_positions,
             walls,
             number_of_walls,
             table_size,
             heat_map,
             connection_points,
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
        new_heat_map,
        new_connection_points
    ) in next_states(
        current_pawns_positions,
        start_positions,
        walls,
        number_of_walls,
        table_size,
        is_player_min,
        heat_map,
        previous_generated_walls,
        connection_points
    ):

        alpha = max(alpha, min_value(new_current_pawns_positions,
                                     new_start_positions,
                                     new_walls,
                                     new_number_of_walls,
                                     new_table_size,
                                     new_heat_map,
                                     new_connection_points,
                                     depth-1,
                                     new_is_player_min,
                                     alpha[-1],
                                     beta[-1],
                                     paths,
                                     previous_generated_walls,
                                     new_current_pawns_positions if state_current_pawns_positions is None else state_current_pawns_positions,
                                     new_walls if state_walls is None else state_walls,
                                     new_number_of_walls if state_number_of_walls is None else state_number_of_walls
                                     ),
                    key=lambda x: x[-1]
                    )
        if alpha[-1] >= beta[-1]:
            return beta

    return alpha


def min_value(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    heat_map: dict[tuple[int, int], int],
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
    depth: int,
    is_player_min: bool,
    alpha: int,
    beta: int,
    paths: tuple[tuple[list[tuple[int, int]], list[tuple[int, int]]], tuple[list[tuple[int, int]], list[tuple[int, int]]]],
    previous_generated_walls: tuple[tuple[tuple[int,  int], ...], tuple[tuple[int, int], ...]],
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
            connection_points,
            depth,
            is_player_min,
            alpha,
            beta,
            state_current_pawns_positions,
            state_walls,
            state_number_of_walls,
            evaluate_state(current_pawns_positions, start_positions,
                           walls, number_of_walls, table_size,paths, heat_map)
        )
    beta = (current_pawns_positions,
            start_positions,
            walls,
            number_of_walls,
            table_size,
            heat_map,
            connection_points,
            depth,
            is_player_min,
            alpha,
            beta,
            state_walls,
            state_number_of_walls,
            beta)
    alpha = (current_pawns_positions,
             start_positions,
             walls,
             number_of_walls,
             table_size,
             heat_map,
             connection_points,
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
        new_heat_map,
        new_connection_points
    ) in next_states(
        current_pawns_positions,
        start_positions,
        walls,
        number_of_walls,
        table_size,
        is_player_min,
        heat_map,
        previous_generated_walls,
        connection_points
    ):
        beta = min(beta, max_value(new_current_pawns_positions,
                                   new_start_positions,
                                   new_walls,
                                   new_number_of_walls,
                                   new_table_size,
                                   new_heat_map,
                                   new_connection_points,
                                   depth-1,
                                   new_is_player_min,
                                   alpha[-1],
                                   beta[-1],
                                   paths,
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
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
    generate_vertical: bool,
    generate_horizontal: bool,
    x_to_move: bool
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    vertical_walls = []
    if generate_vertical:
        for i in range(1, table_size[0]):
            for j in range(1, table_size[1]+1):
                if (i, j) not in walls[0] and is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, (i, j), False, connection_points, x_to_move):
                    vertical_walls.append((i, j))

    horizontal_walls = []
    if generate_horizontal:
        for i in range(1, table_size[0]+1):
            for j in range(1, table_size[1]):
                if (i, j) not in walls[1] and is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, (i, j), True, connection_points, x_to_move):
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
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    all_pawn_positions = generate_pawns_positions(
        current_pawns_positions, start_positions, walls, table_size, is_player_min)
        
    dest_column = start_positions[not is_player_min][0][1]

    pawn_colum = current_pawns_positions[is_player_min][0][1]
    if len(all_pawn_positions[0]) > 5:
        if pawn_colum < dest_column:  # ide ka desno
            all_pawn_positions[0] = list(
                filter(lambda x: x[1] > pawn_colum, all_pawn_positions[0]))  # mozda >=
        elif pawn_colum > dest_column:  # ide ka levo
            all_pawn_positions[0] = list(
                filter(lambda x: x[1] < pawn_colum, all_pawn_positions[0]))

    pawn_colum = current_pawns_positions[is_player_min][1][1]
    if len(all_pawn_positions[1]) > 5:
        if pawn_colum < dest_column:  # ide ka desno
            all_pawn_positions[1] = list(
                filter(lambda x: x[1] > pawn_colum, all_pawn_positions[1]))
        elif pawn_colum > dest_column:  # ide ka levo
            all_pawn_positions[1] = list(
                filter(lambda x: x[1] < pawn_colum, all_pawn_positions[1]))

    return tuple(all_pawn_positions)
