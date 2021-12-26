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
    walls_vertical: list[tuple[int, int]],
    walls_horizontal: list[tuple[int, int]],
    table_rows: int,
    table_columns: int,
    row: int,
    column: int,
    is_horizontal: bool
) -> bool:
    if table_rows == row or table_columns == column:
        return False

    if is_horizontal and ((row, column) in walls_horizontal or (row, column-1) in walls_horizontal or (row, column) in walls_vertical):
        return False

    if not is_horizontal and ((row, column) in walls_vertical or (row-1, column) in walls_vertical or (row, column) in walls_horizontal):
        return False

    return True


def is_player_movement_valid(
    walls_vertical: list[tuple[int, int]],
    walls_horizontal: list[tuple[int, int]],
    dimensions: tuple[int,int],
    pawn_old_pos:tuple[int,int],
    pawn_new_pos:tuple[int,int]
) -> bool:
    if pawn_new_pos[1] < 0 or pawn_new_pos[0] < 0 or pawn_new_pos[1] > dimensions[1] or pawn_new_pos[0] > dimensions[0] or (pawn_old_pos[0] == pawn_new_pos[0] and pawn_old_pos[1] == pawn_new_pos[1]):
        return False
    if abs(pawn_new_pos[1]-pawn_old_pos[1]) > 3 or abs(pawn_new_pos[0]-pawn_old_pos[0]) > 3:
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
                ((pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal) or \
                ((pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_horizontal) or \
                    ((pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal):
                return False
        elif\
                ((pawn_old_pos[0], pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_horizontal) or \
                ((pawn_old_pos[0], pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_horizontal) or \
                ((pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_horizontal):
            return False
    elif pawn_old_pos[0]+1 == pawn_new_pos[0]:
        if pawn_old_pos[1]-1 == pawn_new_pos[1]:
            if\
                ((pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]) in walls_horizontal) or \
                ((pawn_old_pos[0], pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]-1) in walls_horizontal) or \
                    ((pawn_old_pos[0]-1, pawn_old_pos[1]-1) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]) in walls_horizontal):
                return False
        else:
            if\
                ((pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]-1) in walls_horizontal) or \
                ((pawn_old_pos[0], pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]-1) in walls_horizontal) or \
                    ((pawn_old_pos[0]-1, pawn_old_pos[1]) in walls_vertical and (pawn_old_pos[0], pawn_old_pos[1]) in walls_horizontal):
                return False

    return True


def position_occupied(
    pawn1: tuple[int, int],
    pawn2: tuple[int, int],
    row_old: int,
    column_old: int,
    row_new: int,
    column_new: int,
) -> tuple[int, int]:

    if row_old-2 == row_new:
        return (row_new+1, column_new)
    elif row_old+2 == row_new:
        return (row_new-1, column_new)
    elif column_old-2 == column_new:
        return (row_new, column_new+1)
    elif column_old+2 == column_new:
        return (row_new, column_new-1)
    return(row_old, column_new)
    # elif row_old-1==row_new:
    #     if column_old-1==column_new:
    #         print
    #     else:
    #         print
    # elif row_old+1==row_new:
    #     if column_old-1==column_new:
    #         print
    #     else:
    #         print
    # da opet unese poziciju ako je dijagonala zauzeta

    return


def move_player(
    walls_vertical: list[tuple[int, int]],
    walls_horizontal: list[tuple[int, int]],
    my_pawn: tuple[int, int],
    pawn1: tuple[int, int],
    pawn2: tuple[int, int],
    table_rows: int,
    table_columns: int,
    row_new: int,
    column_new: int,
) -> tuple[int, int]:
    row_old = my_pawn[0]
    column_old = my_pawn[1]

    if not is_player_movement_valid(walls_vertical, walls_horizontal, table_rows, table_columns, row_old, column_old, row_new, column_new):
        return my_pawn
    if pawn1 == (row_new, column_new) or pawn2 == (row_new, column_new):
        move = position_occupied(
            pawn1, pawn2, row_old, column_old, row_new, column_new)
    else:
        move = (row_new, column_new)
    return move


def place_wall(
    walls_vertical: list[tuple[int, int]],
    walls_horizontal: list[tuple[int, int]],
    heat_map: dict[str, int],
    table_rows: int,
    table_columns: int,
    row: int,
    column: int,
    is_horizontal: bool
) -> bool:
    if(not is_wall_place_valid(walls_vertical, walls_horizontal, table_rows, table_columns, row, column, is_horizontal)):
        return False
    if is_horizontal:
        walls_horizontal.append((row, column))
    else:
        walls_vertical.append((row, column))

    update_heat_map(heat_map, table_rows, table_columns, row, column)

    return True


def update_heat_map(heat_map: dict[tuple[int, int], int], table_rows: int, table_columns: int, row: int, column: int) -> None:
    position = (row, column)
    heat_map[position] += 1
    # dopuniti!!!!!!!!!!!!
    return
