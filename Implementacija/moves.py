from utility import int_to_table_coordinate


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
    walls_vertical: list[tuple[int, int]],
    walls_horizontal: list[tuple[int, int]],
    dimensions: tuple[int, int],
    pawn_old_pos: tuple[int, int],
    pawn_new_pos: tuple[int, int]
) -> bool:
    if pawn_new_pos[1] < 0 or pawn_new_pos[0] < 0 or pawn_new_pos[1] > dimensions[1] or pawn_new_pos[0] > dimensions[0] or (pawn_old_pos[0] == pawn_new_pos[0] and pawn_old_pos[1] == pawn_new_pos[1]):
        return False
    if abs(pawn_new_pos[1]-pawn_old_pos[1]) > 2 or abs(pawn_new_pos[0]-pawn_old_pos[0]) > 2:
        return False
    if pawn_old_pos[0]-2 == pawn_new_pos[0]:
        if (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal or (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_horizontal or (pawn_old_pos[0]-2, pawn_old_pos[1]) in walls_horizontal or (pawn_old_pos[0]-2, pawn_old_pos[1]-1) in walls_horizontal:
            return False
    elif pawn_old_pos[0]+2 == pawn_new_pos[0]:
        if (pawn_old_pos[0], pawn_old_pos[1]) in walls_horizontal or (pawn_old_pos[0], pawn_old_pos[1]-1) in walls_horizontal or (pawn_old_pos[0]+1, pawn_old_pos[1]) in walls_horizontal or (pawn_old_pos[0]+1, pawn_old_pos[1]-1) in walls_horizontal:
            return False
    elif pawn_old_pos[1]-2 == pawn_new_pos[1]:
        if (pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical or (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_vertical or (pawn_old_pos[0], pawn_old_pos[1]-2) in walls_vertical or (pawn_old_pos[0]-1, pawn_old_pos[1]-2) in walls_vertical:
            return False
    elif pawn_old_pos[1]+2 == pawn_new_pos[1]:
        if (pawn_old_pos[0], pawn_old_pos[1]) in walls_vertical or (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_vertical or (pawn_old_pos[0], pawn_old_pos[1]+1) in walls_vertical or (pawn_old_pos[0]-1, pawn_old_pos[1]+1) in walls_vertical:
            return False
    elif pawn_old_pos[0]-1 == pawn_new_pos[0]:
        if pawn_old_pos[1]-1 == pawn_new_pos[1]:
            if\
                (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_vertical or \
				(pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_horizontal or \
                ((pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal) or \
                ((pawn_old_pos[0]-2, pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0]-2, pawn_old_pos[1]-1) in walls_horizontal):
                return False
        elif\
                ((pawn_old_pos[0], pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_horizontal) or \
                ((pawn_old_pos[0]-2, pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]+1) in walls_horizontal) or \
                (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_vertical or \
				(pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal: 
            return False
    elif pawn_old_pos[0]+1 == pawn_new_pos[0]:
        if pawn_old_pos[1]-1 == pawn_new_pos[1]:
            if\
                (pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical or \
				(pawn_old_pos[0], pawn_old_pos[1]-1) in walls_horizontal or \
                ((pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]) in walls_horizontal) or \
                ((pawn_old_pos[0]+1, pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]-2) in walls_horizontal):
                return False
        else:
            if\
                (pawn_old_pos[0], pawn_old_pos[1]) in walls_vertical or \
				(pawn_old_pos[0], pawn_old_pos[1]) in walls_horizontal or \
                ((pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal) or \
                ((pawn_old_pos[0]+1, pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]+1) in walls_horizontal):
                return False
    return True


def transform_position_if_occupied(old_position: tuple[int, int], new_position: tuple[int, int]) -> tuple[int, int]:

    if(old_position[0] == new_position[0]):
        return (new_position[0], new_position[0] + (-1 if old_position[1] < new_position[1] else 1))

    if(old_position[1] == new_position[1]):
        return (new_position[0] + (-1 if old_position[0] < new_position[0] else 1), new_position[1])


def move_pawn(
    vertical_walls: list[tuple[int, int]],
    horizontal_walls: list[tuple[int, int]],
    old_pawn_position: tuple[int, int],
    oponnents_pawn_positions: tuple[tuple[int, int], tuple[int, int]],
    table_size: tuple[int, int],
    new_pawn_position: tuple[int, int]
) -> tuple[int, int]:
    row_old = old_pawn_position[0]
    column_old = old_pawn_position[1]

    if not is_pawn_move_valid(vertical_walls, horizontal_walls, table_size, row_old, column_old, new_pawn_position):
        return old_pawn_position

    if oponnents_pawn_positions[0] == new_pawn_position or oponnents_pawn_positions[1] == new_pawn_position:
        return transform_position_if_occupied(old_pawn_position, new_pawn_position)

    return new_pawn_position


def place_wall(
    vertical_walls: list[tuple[int, int]],
    horizontal_walls: list[tuple[int, int]],
    heat_map: dict[tuple[int, int], int],
    table_size: tuple[int, int],
    row: int,
    column: int,
    is_horizontal: bool
) -> bool:
    if(not is_wall_place_valid(vertical_walls, horizontal_walls, table_rows, table_columns, row, column, is_horizontal)):
        return False
    if is_horizontal:
        horizontal_walls.append((row, column))
    else:
        vertical_walls.append((row, column))

    update_heat_map(heat_map, table_rows, table_columns, row, column)

    return True


def update_heat_map(heat_map: dict[tuple[int, int], int], table_rows: int, table_columns: int, row: int, column: int) -> None:
    position = (row, column)
    heat_map[position] += 1
    # dopuniti!!!!!!!!!!!!
    return
