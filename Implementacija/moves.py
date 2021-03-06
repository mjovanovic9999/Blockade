from queue import Queue

from frozendict import frozendict
from utility import add_to_tuple, add_wall_in_tuple, remove_from_tuple, remove_neighbor_coordinate_tuple_from_dict, update_coordinate_tuple_dict_neighbors_or_insert_new_node, update_tuple
import path_finding


def is_game_end(
    current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int],
                                 tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]
) -> bool:
    return current_pawn_positions[0][0] in start_positions[1] or current_pawn_positions[0][1] in start_positions[1] or current_pawn_positions[1][0] in start_positions[0] or current_pawn_positions[1][1] in start_positions[0]


def is_wall_place_valid(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    new_wall: tuple[int, int],
    is_wall_horizontal: bool,
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
    x_to_move: bool
) -> bool:
    if table_size[0] <= new_wall[0] or table_size[1] <= new_wall[1] or new_wall[0] < 0 or new_wall[1] < 0:
        return False

    if is_wall_horizontal and \
        (
            new_wall in walls[1] or
            (new_wall[0], new_wall[1] - 1) in walls[1] or
            (new_wall[0], new_wall[1] + 1) in walls[1] or
            new_wall in walls[0]
        ):
        return False

    if not is_wall_horizontal and (
        new_wall in walls[0] or
        (new_wall[0] - 1, new_wall[1]) in walls[0] or
        (new_wall[0] + 1, new_wall[1]) in walls[0] or
        new_wall in walls[1]):
        return False

    start = new_wall
    end1 = None
    end2 = None
    new_walls = add_wall_in_tuple(walls, new_wall, is_wall_horizontal)
    connection_points = update_wall_connection_points(
        connection_points, new_wall, is_wall_horizontal)

    if is_wall_horizontal:
        end1 = (new_wall[0], new_wall[1] - 1)
        end2 = (new_wall[0], new_wall[1] + 1)
    else:
        end1 = (new_wall[0] - 1, new_wall[1])
        end2 = (new_wall[0] + 1, new_wall[1])

    if is_wall_connected_with_two_or_more_walls(new_wall, is_wall_horizontal, table_size, walls) and (path_finding.do_walls_make_polygon(remove_neighbor_coordinate_tuple_from_dict(connection_points, new_wall, end1), start, end1) or path_finding.do_walls_make_polygon(remove_neighbor_coordinate_tuple_from_dict(connection_points, new_wall, end2), start, end2)):
        for player_indices in [(0,0), (0,1), (1,0), (1,1)]:
           for destination_index in [0,1]:
               a = path_finding.a_star(current_pawns_positions, start_positions, new_walls, table_size, player_indices[0],player_indices[1],start_positions[not player_indices[0]][destination_index],{})
               if not a:
                return False
    return True


def is_pawn_move_valid(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,
    old_pawn_position: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> bool:

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
               ((old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] and (old_pawn_position[0], old_pawn_position[1]-1) in walls[1]) or \
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


def is_pawn_move_valid_with_indexes(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,
    new_pawn_position: tuple[int, int]
) -> bool:
    return is_pawn_move_valid(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, current_pawns_positions[selected_player_index][selected_pawn_index], new_pawn_position)


def move_pawn(
    current_pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    new_pawn_position: tuple[int, int],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int
) -> tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]]:
    if not is_pawn_move_valid_with_indexes(current_pawn_positions,
                                           start_positions,
                                           walls,
                                           table_size,
                                           selected_player_index,
                                           selected_pawn_index,
                                           new_pawn_position):
        return current_pawn_positions

    return update_tuple(current_pawn_positions,
                        selected_player_index,
                        update_tuple(current_pawn_positions[selected_player_index],
                                     selected_pawn_index,
                                     new_pawn_position))


def place_wall(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    heat_map: dict[tuple[int, int], int],
    table_size: tuple[int, int],
    wall_position: tuple[int, int],
    wall_index: int,
    player_index: int,
    connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]]
) -> tuple[tuple[tuple, tuple], tuple[tuple[int, int], tuple[int, int]], dict[tuple[int, int], int]]:
    if not is_wall_place_valid(current_pawns_positions, start_positions, walls, table_size, wall_position, wall_index, connection_points, not player_index):
        return (walls, number_of_walls, heat_map, connection_points)

    # new_heatmap = update_heat_map(heat_map, table_size, wall_position)

    return (update_tuple(walls,
                         wall_index,
                         add_to_tuple(walls[wall_index], wall_position)),
            update_tuple(number_of_walls,
                         player_index,
                         update_tuple(number_of_walls[player_index],
                                      wall_index,
                                      number_of_walls[player_index][wall_index] - 1)),
            {},
            update_wall_connection_points(connection_points, wall_position, wall_index))


def update_wall_connection_points(wall_connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
                                  new_wall_position: tuple[int, int],
                                  is_horizontal: bool) -> frozendict[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], ...]]:
    wall_connection_points_dict = dict(wall_connection_points)
    new_wall_position = update_tuple(
        new_wall_position, is_horizontal, new_wall_position[is_horizontal] - 1)

    new_wall_position = add_neighbor_connection_point(
        new_wall_position, is_horizontal, wall_connection_points_dict)

    add_neighbor_connection_point(
        new_wall_position, is_horizontal, wall_connection_points_dict)

    return frozendict(wall_connection_points_dict)


def add_neighbor_connection_point(new_connection_point: tuple[int, int], is_horizontal: bool, wall_connection_points: dict[tuple[int, int], tuple[tuple[int, int], ...]]) -> tuple[int, int]:
    new_connection_points = (
        new_connection_point, (new_connection_point[0], new_connection_point[1] + 1) if is_horizontal else (new_connection_point[0] + 1, new_connection_point[1]))

    update_coordinate_tuple_dict_neighbors_or_insert_new_node(
        wall_connection_points, new_connection_points[0], new_connection_points[1])
    update_coordinate_tuple_dict_neighbors_or_insert_new_node(
        wall_connection_points, new_connection_points[1], new_connection_points[0])

    return new_connection_points[1]


def generate_border_connection_points(table_size: tuple[int, int]) -> frozendict[tuple[int, int], tuple[tuple[int, int], ...]]:
    border_connection_points = {}
    right_border = table_size[1] - 1
    bot_border = table_size[0] - 1

    border_connection_points[(0, 0)] = ((1, 0), (0, 1))

    for width in range(1, table_size[1]):
        border_connection_points[(0, width)] = ((0, width - 1), (0, width + 1))
        border_connection_points[(table_size[0], width)] = (
            (table_size[0], width - 1), (table_size[0], width + 1))

    border_connection_points[(0, table_size[1])] = (
        (0, right_border), (1, table_size[1]))
    border_connection_points[(table_size[0], 0)] = (
        (table_size[0], 1), (bot_border, 0))

    for height in range(1, table_size[0]):
        border_connection_points[(height, 0)] = (
            (height - 1, 0), (height + 1, 0))
        border_connection_points[(height, table_size[1])] = (
            (height - 1, table_size[1]), (height + 1, table_size[1]))

    border_connection_points[table_size] = (
        (bot_border, table_size[1]), (table_size[0], right_border))

    return frozendict(border_connection_points)


def update_heat_map(heat_map: dict[tuple[int, int], int], table_size: tuple[int, int], wall_position: tuple[int, int]) -> dict[tuple[int, int], int]:
    # position = (row, column)
    # heat_map[position] += 1
    # dopuniti!!!!!!!!!!!!
    return heat_map


def is_wall_connected_with_two_or_more_walls(wall: tuple[int, int],
                                             is_horizontal: bool,
                                             table_size: tuple[int, int],
                                             walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]) -> bool:

    if is_horizontal:
        left_neighbor = wall[1] == 1
        right_neighbor = wall[1] + 1 == table_size[1]
        middle_neighbor = False
        for horizontal_wall in walls[1]:
            if not left_neighbor and horizontal_wall[0] == wall[0] and horizontal_wall[1] == wall[1] - 2:
                left_neighbor = True
            if not right_neighbor and horizontal_wall[0] == wall[0] and horizontal_wall[1] == wall[1] + 2:
                right_neighbor = True
            counter = 0
            for neighbor in [left_neighbor, middle_neighbor, right_neighbor]:
                if neighbor:
                    counter += 1
            if counter >= 2:
                return True  

        for vertical_wall in walls[0]:
            if not left_neighbor and vertical_wall[1] == wall[1] - 1 and (vertical_wall[0] == wall[0] or vertical_wall[0] == wall[0] - 1 or vertical_wall[0] == wall[0] + 1):
                left_neighbor = True
            if not right_neighbor and vertical_wall[1] == wall[1] + 1 and (vertical_wall[0] == wall[0] or vertical_wall[0] == wall[0] - 1 or vertical_wall[0] == wall[0] + 1):
                right_neighbor = True
            if vertical_wall[1] == wall[1] and (vertical_wall[0] == wall[0] + 1 or vertical_wall[0] == wall[0] - 1):
                middle_neighbor = True
            counter = 0
            for neighbor in [left_neighbor, middle_neighbor, right_neighbor]:
                if neighbor:
                    counter += 1
            if counter >= 2:
                return True  
    else:
        top_neighbor = wall[0] == 1
        bottom_neighbor = wall[0] + 1 == table_size[0]
        middle_neighbor = False
        for horizontal_wall in walls[1]:
            if not top_neighbor and horizontal_wall[0] == wall[0] - 1 and (horizontal_wall[1] == wall[1] or horizontal_wall[1] == wall[1] - 1 or horizontal_wall[1] == wall[1] + 1):
                top_neighbor = True
            if not bottom_neighbor and horizontal_wall[0] == wall[0] + 1 and (horizontal_wall[1] == wall[1] or horizontal_wall[1] == wall[1] - 1 or horizontal_wall[1] == wall[1] + 1):
                bottom_neighbor = True
            if horizontal_wall[0] == wall[0] and (horizontal_wall[1] == wall[1] + 1 or horizontal_wall[1] == wall[1] - 1):
                middle_neighbor = True
            counter = 0
            for neighbor in [top_neighbor, middle_neighbor, bottom_neighbor]:
                if neighbor:
                    counter += 1
            if counter >= 2:
                return True
        for vertical_wall in walls[0]:
            if not top_neighbor and vertical_wall[1] == wall[1] and vertical_wall[0] == wall[0] - 2:
                top_neighbor = True
            if not bottom_neighbor and vertical_wall[1] == wall[1] and vertical_wall[0] == wall[0] + 2:
                bottom_neighbor = True
            counter = 0
            for neighbor in [top_neighbor, middle_neighbor, bottom_neighbor]:
                if neighbor:
                    counter += 1
            if counter >= 2:
                return True
    return False
        