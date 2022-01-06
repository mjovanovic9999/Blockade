from queue import Queue
from utility import add_to_tuple, update_tuple


def is_game_end(
    current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int],
                                 tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]
) -> bool:
    return current_pawn_positions[0][0] in start_positions[1] or current_pawn_positions[0][1] in start_positions[1] or current_pawn_positions[1][0] in start_positions[0] or current_pawn_positions[1][1] in start_positions[0]


def is_wall_place_valid(
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    wall_position: tuple[int, int],
    is_horizontal: bool
) -> bool:
    if table_size[0] <= wall_position[0] or table_size[1] <= wall_position[1] or wall_position[0] < 0 or wall_position[1] < 0:
        return False

    if is_horizontal and (wall_position in walls[1] or (wall_position[0], wall_position[1] - 1) in walls[1] or (wall_position[0], wall_position[1] + 1) in walls[1] or wall_position in walls[0]):
        return False

    if not is_horizontal and (wall_position in walls[0] or (wall_position[0] - 1, wall_position[1]) in walls[0] or (wall_position[0] + 1, wall_position[1]) in walls[0] or wall_position in walls[1]):
        return False

    return True


def is_pawn_move_valid(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,  # da se izbaci mzd
    old_pawn_position: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> bool:
    # da moze da ga istera!!!!!!!!!!!!!!!!!!!!!!

    if new_pawn_position[1] < 1 or new_pawn_position[0] < 1 or new_pawn_position[1] > table_size[1] or new_pawn_position[0] > table_size[0] or (old_pawn_position[0] == new_pawn_position[0] and old_pawn_position[1] == new_pawn_position[1]):
        return False
    if abs(new_pawn_position[1]-old_pawn_position[1]) + abs(new_pawn_position[0]-old_pawn_position[0]) > 2:
        return False

    all_pawns = list(current_pawns_positions[0]+current_pawns_positions[1])
    all_pawns.remove(
        current_pawns_positions[selected_player_index][selected_pawn_index])

    if new_pawn_position in list(current_pawns_positions[selected_player_index]):
        return False

    my_both_destinations = list(start_positions[not selected_player_index])

    if new_pawn_position in list(current_pawns_positions[not selected_player_index]) and not new_pawn_position in my_both_destinations:
        return False

    if old_pawn_position[0]-2 == new_pawn_position[0]:
        if\
            (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1] or\
            (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1] or\
            (old_pawn_position[0]-2, old_pawn_position[1]) in walls[1] or\
                (old_pawn_position[0]-2, old_pawn_position[1]-1) in walls[1]:
            return False
    elif old_pawn_position[0]+2 == new_pawn_position[0]:
        if\
            (old_pawn_position[0], old_pawn_position[1]) in walls[1] or\
            (old_pawn_position[0], old_pawn_position[1]-1) in walls[1] or\
            (old_pawn_position[0]+1, old_pawn_position[1]) in walls[1] or\
                (old_pawn_position[0]+1, old_pawn_position[1]-1) in walls[1]:
            return False
    elif old_pawn_position[1]-2 == new_pawn_position[1]:
        if\
            (old_pawn_position[0], old_pawn_position[1]-1) in walls[0] or\
            (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] or\
            (old_pawn_position[0], old_pawn_position[1]-2) in walls[0] or\
                (old_pawn_position[0]-1, old_pawn_position[1]-2) in walls[0]:
            return False
    elif old_pawn_position[1]+2 == new_pawn_position[1]:
        if\
            (old_pawn_position[0], old_pawn_position[1]) in walls[0] or\
            (old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] or\
            (old_pawn_position[0], old_pawn_position[1]+1) in walls[0] or\
                (old_pawn_position[0]-1, old_pawn_position[1]+1) in walls[0]:
            return False

    elif old_pawn_position[0]-1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] or \
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1] or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1]) or \
                ((old_pawn_position[0]-2, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]-2) in walls[1]) or\
                ((old_pawn_position[0]-2, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0], old_pawn_position[1]-1) in walls[0]) or\
                    ((old_pawn_position[0]-1, old_pawn_position[1]-2) in walls[1] and (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1]):
                return False
        elif old_pawn_position[1]+1 == new_pawn_position[1]:
            if\
                ((old_pawn_position[0], old_pawn_position[1]) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1]) or \
                ((old_pawn_position[0]-2, old_pawn_position[1]) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]+1) in walls[1]) or \
                (old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] or \
                (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1] or\
                ((old_pawn_position[0]-2, old_pawn_position[1]) in walls[0] and (old_pawn_position[0], old_pawn_position[1]) in walls[0]) or\
                    ((old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1] and (old_pawn_position[0]-1, old_pawn_position[1]+1) in walls[1]):
                return False
        else:  # samo ako je piun za 2 gore
            if\
                not ((old_pawn_position[0]-2, old_pawn_position[1]) in all_pawns or
                     (old_pawn_position[0]-1, old_pawn_position[1]) in my_both_destinations) or\
                ((old_pawn_position[0]-1, old_pawn_position[1]) in walls[1] or
                 (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1]):
                return False
    elif old_pawn_position[0]+1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0], old_pawn_position[1]-1) in walls[0] or \
                (old_pawn_position[0], old_pawn_position[1]-1) in walls[1] or \
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0], old_pawn_position[1]) in walls[1]) or \
                ((old_pawn_position[0]+1, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0], old_pawn_position[1]-2) in walls[1]) or\
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]+1, old_pawn_position[1]-1) in walls[0]) or\
                    ((old_pawn_position[0], old_pawn_position[1]-2) in walls[1] and (old_pawn_position[0], old_pawn_position[1]) in walls[1]):
                return False
        elif old_pawn_position[1]+1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0], old_pawn_position[1]) in walls[0] or \
                (old_pawn_position[0], old_pawn_position[1]) in walls[1] or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1]) or \
                ((old_pawn_position[0]+1, old_pawn_position[1]) in walls[0] and (old_pawn_position[0], old_pawn_position[1]+1) in walls[1]) or\
                ((old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] and (old_pawn_position[0]+1, old_pawn_position[1]) in walls[0]) or\
                    ((old_pawn_position[0], old_pawn_position[1]-1) in walls[1] and (old_pawn_position[0], old_pawn_position[1]+1) in walls[1]):
                return False
        else:  # samo ako je piun za 2 dole
            if\
                not ((old_pawn_position[0]+2, old_pawn_position[1]) in all_pawns or
                     (old_pawn_position[0]+1, old_pawn_position[1]) in my_both_destinations) or\
                ((old_pawn_position[0], old_pawn_position[1]) in walls[1] or
                 (old_pawn_position[0], old_pawn_position[1]-1) in walls[1]):
                return False
    # ako je pesak na +-2 po levo pa desno
    elif old_pawn_position[1]-1 == new_pawn_position[1]:
        if\
            not ((old_pawn_position[0], old_pawn_position[1]-2) in all_pawns or
                 (old_pawn_position[0], old_pawn_position[1]-1) in my_both_destinations) or\
            ((old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] or
             (old_pawn_position[0], old_pawn_position[1]-1) in walls[0]):
            return False
    elif old_pawn_position[1]+1 == new_pawn_position[1]:
        if\
            not ((old_pawn_position[0], old_pawn_position[1]+2) in all_pawns or
                 (old_pawn_position[0], old_pawn_position[1]+1) in my_both_destinations) or\
            (old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] or\
                (old_pawn_position[0], old_pawn_position[1]) in walls[0]:
            return False
    return True


def transform_position_if_occupied(old_position: tuple[int, int], new_position: tuple[int, int]) -> tuple[int, int]:

    if(old_position[0] == new_position[0]):
        return (new_position[0], new_position[1] + (-1 if old_position[1] < new_position[1] else 1))

    if(old_position[1] == new_position[1]):
        return (new_position[0] + (-1 if old_position[0] < new_position[0] else 1), new_position[1])

    return old_position


def transform_position_if_pawn_skips_start_position(new_position: tuple[int, int], opponent_start_positions: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int]:
    if(new_position[0] == new_position[0]):
        return (new_position[0], new_position[1] + (-1 if new_position[1] < new_position[1] else 1))


def move_pawn(
    current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    new_pawn_position: tuple[int, int],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int
) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    if not is_pawn_move_valid(current_pawn_positions,
                              start_positions,
                              walls,
                              table_size,
                              selected_player_index,
                              selected_pawn_index,
                              current_pawn_positions[selected_player_index][selected_pawn_index],
                              new_pawn_position):
        return current_pawn_positions

    return update_tuple(current_pawn_positions,
                        selected_player_index,
                        update_tuple(current_pawn_positions[selected_player_index],
                                     selected_pawn_index,
                                     new_pawn_position))


def place_wall(
    walls: tuple[tuple, tuple],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    heat_map: dict[tuple[int, int], int],
    table_size: tuple[int, int],
    wall_position: tuple[int, int],
    wall_index: int,
    player_index: int
) -> tuple[tuple[tuple, tuple], tuple[tuple[int, int], tuple[int, int]], dict[tuple[int, int], int]]:
    if not is_wall_place_valid(walls, table_size, wall_position, wall_index == 1):
        return (walls, number_of_walls, heat_map)

    new_heatmap = update_heat_map(heat_map, table_size, wall_position)

    return (update_tuple(walls,
                         wall_index,
                         add_to_tuple(walls[wall_index], wall_position)),
            update_tuple(number_of_walls,
                         player_index,
                         update_tuple(number_of_walls[player_index],
                                      wall_index,
                                      number_of_walls[player_index][wall_index] - 1)),
            new_heatmap)


def update_heat_map(heat_map: dict[tuple[int, int], int], table_size: tuple[int, int], wall_position: tuple[int, int]) -> dict[tuple[int, int], int]:
    # position = (row, column)
    # heat_map[position] += 1
    # dopuniti!!!!!!!!!!!!
    return heat_map


def is_wall_connected_with_two_or_more_walls(wall: tuple[int, int],
                                             is_horizontal: bool,
                                             table_size: tuple[int, int],
                                             walls: tuple[tuple, tuple]) -> bool:

    if is_horizontal:
        left_neighbor = wall[1] == 1
        right_neighbor = wall[1] + 1 == table_size[1]
        for horizontal_wall in walls[1]:
            if not left_neighbor and horizontal_wall[0] == wall[0] and horizontal_wall[1] == wall[1] - 2:
                left_neighbor = True
            if not right_neighbor and horizontal_wall[0] == wall[0] and horizontal_wall[1] == wall[1] + 2:
                right_neighbor = True
            if right_neighbor and left_neighbor:
                return True

        for vertical_wall in walls[0]:
            if not left_neighbor and vertical_wall[1] == wall[1] - 1 and (vertical_wall[0] == wall[0] or vertical_wall[0] == wall[0] - 1 or vertical_wall[0] == wall[0] + 1):
                left_neighbor = True
            if not right_neighbor and vertical_wall[1] == wall[1] + 1 and (vertical_wall[0] == wall[0] or vertical_wall[0] == wall[0] - 1 or vertical_wall[0] == wall[0] + 1):
                right_neighbor = True
            if right_neighbor and left_neighbor:
                return True

    else:
        top_neighbor = wall[0] == 1
        bottom_neighbor = wall[0] + 1 == table_size[0]
        for horizontal_wall in walls[1]:
            if not top_neighbor and horizontal_wall[0] == wall[0] - 1 and (horizontal_wall[1] == wall[1] or horizontal_wall[1] == wall[1] - 1 or horizontal_wall[1] == wall[1] + 1):
                top_neighbor = True
            if not bottom_neighbor and horizontal_wall[0] == wall[0] + 1 and (horizontal_wall[1] == wall[1] or horizontal_wall[1] == wall[1] - 1 or horizontal_wall[1] == wall[1] + 1):
                bottom_neighbor = True
            if bottom_neighbor and top_neighbor:
                return True

        for vertical_wall in walls[0]:
            if not top_neighbor and vertical_wall[1] == wall[1] and vertical_wall[0] == wall[0] - 2:
                top_neighbor = True
            if not bottom_neighbor and vertical_wall[1] == wall[1] and vertical_wall[0] == wall[0] + 2:
                bottom_neighbor = True
            if bottom_neighbor and top_neighbor:
                return True

    return False


def get_pawns_for_path_finding(wall: tuple[int, int],
                               is_horizontal: bool,
                               walls: tuple[tuple, tuple],
                               paths: tuple[tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]], tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]],
                               table_size: tuple[int, int]) -> list[tuple[int, int]]:
    pawns_for_path_finding = []
    visited_walls = set()
    walls_to_visit = Queue()

    for wall in get_neighbor_walls_indexes(wall, is_horizontal, walls):
        walls_to_visit.put(wall)

    print(walls_to_visit)

    while not walls_to_visit.empty() and len(pawns_for_path_finding) < 4:
        current_wall_tuple = walls_to_visit.get()
        current_wall = walls[current_wall[0]][current_wall[1]]
        is_horizontal = current_wall[0] == 1
        visited_walls.add(current_wall_tuple)

        if is_wall_connected_with_two_or_more_walls(current_wall, is_horizontal, table_size):
            for wall in get_neighbor_walls_indexes(wall, is_horizontal, walls):
                if wall not in visited_walls:
                    walls_to_visit.put(wall)

        pass

    return pawns_for_path_finding


def get_indexes_of_pawns_whose_path_is_cut(wall: tuple[int, int],
                                           is_horizontal: bool,
                                           paths: tuple[tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]], tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]]) -> list:
    pass


def get_neighbor_walls_indexes(wall: tuple[int, int],
                               is_horizontal: bool,
                               walls: tuple[tuple, tuple]) -> list[tuple[int, int]]:
    neighbors = []

    if is_horizontal:
        for index, horizontal_wall in enumerate(walls[1]):
            if horizontal_wall[0] == wall[0] and (horizontal_wall[1] == wall[1] - 2 or horizontal_wall[1] == wall[1] + 2):
                neighbors.append((1, index))

        for index, vertical_wall in enumerate(walls[0]):
            if (vertical_wall[1] == wall[1] - 1 or vertical_wall[1] == wall[1] + 1 or vertical_wall[1] == wall[1]) and (vertical_wall[0] == wall[0] or vertical_wall[0] == wall[0] - 1 or vertical_wall[0] == wall[0] + 1):
                neighbors.append((0, index))

    else:
        for index, horizontal_wall in enumerate(walls[1]):
            if (horizontal_wall[0] == wall[0] - 1 or horizontal_wall[0] == wall[0] + 1) and (horizontal_wall[1] == wall[1] or horizontal_wall[1] == wall[1] - 1 or horizontal_wall[1] == wall[1] + 1):
                neighbors.append((1, index))

        for index, vertical_wall in enumerate(walls[0]):
            if vertical_wall[1] == wall[1] and (vertical_wall[0] == wall[0] - 2 or vertical_wall[0] == wall[0] + 2):
                neighbors.append((0, index))

    return neighbors
