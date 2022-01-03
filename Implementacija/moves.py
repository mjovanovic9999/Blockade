from utility import int_to_table_coordinate
from copy import deepcopy


def is_game_end(
    pawn_x1: tuple[int, int],
    pawn_x2: tuple[int, int],
    pawn_o1: tuple[int, int],
    pawn_o2: tuple[int, int],
    start_positions_x: tuple[tuple[int, int], tuple[int, int]],
    start_positions_o: tuple[tuple[int, int], tuple[int, int]]
) -> bool:
    return pawn_x1 in start_positions_o or pawn_x2 in start_positions_o or pawn_o1 in start_positions_x or pawn_o2 in start_positions_x


def is_wall_place_valid(
    vertical_walls: list[tuple[int, int]],
    horizontal_walls: list[tuple[int, int]],
    table_size: tuple[int, int],
    wall_position: tuple[int, int],
    is_horizontal: bool
) -> bool:
    if table_size[0] <= wall_position[0] or table_size[1] <= wall_position[1] or wall_position[0] < 0 or wall_position[1] < 0:
        return False

    if is_horizontal and (wall_position in horizontal_walls or (wall_position[0], wall_position[1] - 1) in horizontal_walls or (wall_position[0], wall_position[1] + 1) in horizontal_walls or wall_position in vertical_walls):
        return False

    if not is_horizontal and (wall_position in vertical_walls or (wall_position[0] - 1, wall_position[1]) in vertical_walls or (wall_position[0] + 1, wall_position[1]) in vertical_walls or wall_position in horizontal_walls):
        return False

    return True


def is_pawn_move_valid(
    vertical_walls: list[tuple[int, int]],
    horizontal_walls: list[tuple[int, int]],
    table_size: tuple[int, int],
    old_pawn_position: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> bool:
    if new_pawn_position[1] < 0 or new_pawn_position[0] < 0 or new_pawn_position[1] > table_size[1]-1 or new_pawn_position[0] > table_size[0]-1 or (old_pawn_position[0] == new_pawn_position[0] and old_pawn_position[1] == new_pawn_position[1]):
        return False
    if abs(new_pawn_position[1]-old_pawn_position[1]) + abs(new_pawn_position[0]-old_pawn_position[0]) > 2:
        return False
    if old_pawn_position[0]-2 == new_pawn_position[0]:
        if (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls or (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls or (old_pawn_position[0]-2, old_pawn_position[1]) in horizontal_walls or (old_pawn_position[0]-2, old_pawn_position[1]-1) in horizontal_walls:
            return False
    elif old_pawn_position[0]+2 == new_pawn_position[0]:
        if (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls or (old_pawn_position[0], old_pawn_position[1]-1) in horizontal_walls or (old_pawn_position[0]+1, old_pawn_position[1]) in horizontal_walls or (old_pawn_position[0]+1, old_pawn_position[1]-1) in horizontal_walls:
            return False
    elif old_pawn_position[1]-2 == new_pawn_position[1]:
        if (old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls or (old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls or (old_pawn_position[0], old_pawn_position[1]-2) in vertical_walls or (old_pawn_position[0]-1, old_pawn_position[1]-2) in vertical_walls:
            return False
    elif old_pawn_position[1]+2 == new_pawn_position[1]:
        if (old_pawn_position[0], old_pawn_position[1]) in vertical_walls or (old_pawn_position[0]-1, old_pawn_position[1]) in vertical_walls or (old_pawn_position[0], old_pawn_position[1]+1) in vertical_walls or (old_pawn_position[0]-1, old_pawn_position[1]+1) in vertical_walls:
            return False
    elif old_pawn_position[0]-1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls or \
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls) or \
                    ((old_pawn_position[0]-2, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]-2) in horizontal_walls):
                return False
        elif\
                ((old_pawn_position[0], old_pawn_position[1]) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]-1) in horizontal_walls) or \
                ((old_pawn_position[0]-2, old_pawn_position[1]) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]+1) in horizontal_walls) or \
                (old_pawn_position[0]-1, old_pawn_position[1]) in vertical_walls or \
            (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls:
            return False
    elif old_pawn_position[0]+1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls or \
                (old_pawn_position[0], old_pawn_position[1]-1) in horizontal_walls or \
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls) or \
                    ((old_pawn_position[0]+1, old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]-2) in horizontal_walls):
                return False
        else:
            if\
                (old_pawn_position[0], old_pawn_position[1]) in vertical_walls or \
                (old_pawn_position[0], old_pawn_position[1]) in horizontal_walls or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in vertical_walls and (old_pawn_position[0]-1, old_pawn_position[1]) in horizontal_walls) or \
                    ((old_pawn_position[0]+1, old_pawn_position[1]) in vertical_walls and (old_pawn_position[0], old_pawn_position[1]+1) in horizontal_walls):
                return False
    return True


def transform_position_if_occupied(old_position: tuple[int, int], new_position: tuple[int, int]) -> tuple[int, int]:

    if(old_position[0] == new_position[0]):
        return (new_position[0], new_position[1] + (-1 if old_position[1] < new_position[1] else 1))

    if(old_position[1] == new_position[1]):
        return (new_position[0] + (-1 if old_position[0] < new_position[0] else 1), new_position[1])

    return old_position


def move_pawn(
    vertical_walls: list[tuple[int, int]],
    horizontal_walls: list[tuple[int, int]],
    old_pawn_position: tuple[int, int],
    oponnents_pawn_positions: tuple[tuple[int, int], tuple[int, int]],
    other_pawn_position: tuple[int, int],
    table_size: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> tuple[int, int]:
    if not is_pawn_move_valid(vertical_walls, horizontal_walls, table_size, old_pawn_position, new_pawn_position):
        return old_pawn_position

    if oponnents_pawn_positions[0] == new_pawn_position or oponnents_pawn_positions[1] == new_pawn_position or other_pawn_position == new_pawn_position:
        return transform_position_if_occupied(old_pawn_position, new_pawn_position)

    return new_pawn_position


def place_wall(
    vertical_walls: list[tuple[int, int]],
    horizontal_walls: list[tuple[int, int]],
    heat_map: dict[tuple[int, int], int],
    table_size: tuple[int, int],
    wall_position: tuple[int, int],
    is_horizontal: bool
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], dict[tuple[int, int], int]]:
    if(not is_wall_place_valid(vertical_walls, horizontal_walls, table_size, wall_position, is_horizontal)):
        return (vertical_walls, horizontal_walls, heat_map)

    new_vertical_walls = deepcopy(vertical_walls)
    new_horizontal_walls = deepcopy(horizontal_walls)

    if is_horizontal:
        new_horizontal_walls.append(wall_position)
    else:
        new_vertical_walls.append(wall_position)

    new_heatmap = update_heat_map(heat_map, table_size, wall_position)

    return (new_vertical_walls, new_horizontal_walls, new_heatmap)


def update_heat_map(heat_map: dict[tuple[int, int], int], table_size: tuple[int, int], wall_position: tuple[int, int]) -> dict[tuple[int, int], int]:
    # position = (row, column)
    # heat_map[position] += 1
    # dopuniti!!!!!!!!!!!!
    return heat_map