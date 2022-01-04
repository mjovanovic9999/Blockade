from utility import int_to_table_coordinate, update_tuple
from copy import deepcopy


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

    if is_horizontal and (wall_position in walls[1] or (wall_position[0], wall_position[1] - 1) in walls[1] or (wall_position[0], wall_position[1] + 1) in walls[1] or wall_position in walls[1]):
        return False

    if not is_horizontal and (wall_position in walls[0] or (wall_position[0] - 1, wall_position[1]) in walls[0] or (wall_position[0] + 1, wall_position[1]) in walls[0] or wall_position in walls[0]):
        return False

    return True


def is_pawn_move_valid(
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    old_pawn_position: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> bool:
    if new_pawn_position[1] < 0 or new_pawn_position[0] < 0 or new_pawn_position[1] > table_size[1]-1 or new_pawn_position[0] > table_size[0]-1 or (old_pawn_position[0] == new_pawn_position[0] and old_pawn_position[1] == new_pawn_position[1]):
        return False
    if abs(new_pawn_position[1]-old_pawn_position[1]) + abs(new_pawn_position[0]-old_pawn_position[0]) > 2:
        return False
    if old_pawn_position[0]-2 == new_pawn_position[0]:
        if\
        (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls or\
        (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls or\
        (old_pawn_position[0]-2, old_pawn_position[1]) in horizontal_walls or\
        (old_pawn_position[0]-2, old_pawn_position[1]-1) in horizontal_walls:
            return False
    elif old_pawn_position[0]+2 == new_pawn_position[0]:
        if\
            (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls or\
            (old_pawn_position[0], old_pawn_position[1]-1) in horizontal_walls or\
            (old_pawn_position[0]+1, old_pawn_position[1]) in horizontal_walls or\
            (old_pawn_position[0]+1, old_pawn_position[1]-1) in horizontal_walls:
            return False
    elif old_pawn_position[1]-2 == new_pawn_position[1]:
        if\
            (old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls or\
            (old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls or\
            (old_pawn_position[0], old_pawn_position[1]-2) in vertical_walls or\
            (old_pawn_position[0]-1, old_pawn_position[1]-2) in vertical_walls:
            return False
    elif old_pawn_position[1]+2 == new_pawn_position[1]:
        if\
            (old_pawn_position[0], old_pawn_position[1]) in vertical_walls or\
            (old_pawn_position[0]-1, old_pawn_position[1]) in vertical_walls or\
            (old_pawn_position[0], old_pawn_position[1]+1) in vertical_walls or\
            (old_pawn_position[0]-1, old_pawn_position[1]+1) in vertical_walls:
            return False
    elif old_pawn_position[0]-1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls or \
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls) or \
                ((old_pawn_position[0]-2, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]-2) in horizontal_walls)or\
                ((old_pawn_position[0]-2, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls)or\
                ((old_pawn_position[0]-1, old_pawn_position[1]-2) in horizontal_walls and (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls):
                return False
        elif\
                ((old_pawn_position[0], old_pawn_position[1]) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls) or \
                ((old_pawn_position[0]-2, old_pawn_position[1]) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]+1) in horizontal_walls) or \
                (old_pawn_position[0]-1, old_pawn_position[1]) in vertical_walls or \
                (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls or\
                ((old_pawn_position[0]-2, old_pawn_position[1]) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]) in vertical_walls)or\
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls and (old_pawn_position[0]-1, old_pawn_position[1]+1) in horizontal_walls):
                return False
    elif old_pawn_position[0]+1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls or \
                (old_pawn_position[0], old_pawn_position[1]-1) in horizontal_walls or \
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls) or \
                ((old_pawn_position[0]+1, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]-2) in horizontal_walls)or\
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]+1, old_pawn_position[1]-1) in vertical_walls)or\
                ((old_pawn_position[0], old_pawn_position[1]-2) in horizontal_walls and (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls):
                return False
        else:
            if\
                (old_pawn_position[0], old_pawn_position[1]) in vertical_walls or \
                (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls) or \
                ((old_pawn_position[0]+1, old_pawn_position[1]) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]+1) in horizontal_walls) or\
                ((old_pawn_position[0]-1, old_pawn_position[1]) in vertical_walls and (old_pawn_position[0]+1, old_pawn_position[1]) in vertical_walls)or\
                ((old_pawn_position[0], old_pawn_position[1]-1) in horizontal_walls and (old_pawn_position[0], old_pawn_position[1]+1) in horizontal_walls):
                return False
        #pomeraj za jednu poziciju na dest (ne dijagonalno)       
    elif old_pawn_position[0]-1 == new_pawn_position[0]:
        if\
        (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls or\
        (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls:
            return False  
    elif old_pawn_position[0]+1 == new_pawn_position[0]:
        if\
        (old_pawn_position[0], old_pawn_position[1]-1) in horizontal_walls or\
        (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls:
            return False
    elif old_pawn_position[1]-1 == new_pawn_position[1]:
        if\
        (old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls or\
        (old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls:
            return False 
    elif old_pawn_position[1]+1 == new_pawn_position[1]:
        if\
        (old_pawn_position[0]-1, old_pawn_position[1]) in vertical_walls or\
        (old_pawn_position[0], old_pawn_position[1]) in vertical_walls:
            return False 
    return True#nije uvek npr uslov za skok na 0 1 na dst


def transform_position_if_occupied(old_position: tuple[int, int], new_position: tuple[int, int]) -> tuple[int, int]:

    if(old_position[0] == new_position[0]):
        return (new_position[0], new_position[1] + (-1 if old_position[1] < new_position[1] else 1))

    if(old_position[1] == new_position[1]):
        return (new_position[0] + (-1 if old_position[0] < new_position[0] else 1), new_position[1])

    return old_position


def move_pawn(
    walls: tuple[tuple, tuple],
    old_pawn_position: tuple[int, int],
    oponnents_pawn_positions: tuple[tuple[int, int], tuple[int, int]],
    other_pawn_position: tuple[int, int],
    table_size: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> tuple[int, int]:
    if not is_pawn_move_valid(walls, table_size, old_pawn_position, new_pawn_position):
        return old_pawn_position

    if oponnents_pawn_positions[0] == new_pawn_position or oponnents_pawn_positions[1] == new_pawn_position or other_pawn_position == new_pawn_position:
        return transform_position_if_occupied(old_pawn_position, new_pawn_position)

    return new_pawn_position


def place_wall(
    walls: tuple[tuple, tuple],
    number_of_walls: tuple[tuple[int, int], tuple[int, int]],
    heat_map: dict[tuple[int, int], int],
    table_size: tuple[int, int],
    wall_position: tuple[int, int],
    is_horizontal: bool,
    x_to_move: bool
) -> tuple[tuple[tuple, tuple], tuple[tuple[int, int], tuple[int, int]], dict[tuple[int, int], int]]:
    if(not is_wall_place_valid(walls, table_size, wall_position, is_horizontal)):
        return (walls, heat_map)

    wall_index = 1 if is_horizontal else 0
    player_index = 0 if x_to_move else 1
    new_heatmap = update_heat_map(heat_map, table_size, wall_position)

    return (update_tuple(walls,
                         wall_index,
                         walls[wall_index] + wall_position),
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
