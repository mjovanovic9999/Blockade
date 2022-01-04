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
        if (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1] or (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1] or (old_pawn_position[0]-2, old_pawn_position[1]) in walls[1] or (old_pawn_position[0]-2, old_pawn_position[1]-1) in walls[1]:
            return False
    elif old_pawn_position[0]+2 == new_pawn_position[0]:
        if (old_pawn_position[0], old_pawn_position[1]) in walls[1] or (old_pawn_position[0], old_pawn_position[1]-1) in walls[1] or (old_pawn_position[0]+1, old_pawn_position[1]) in walls[1] or (old_pawn_position[0]+1, old_pawn_position[1]-1) in walls[1]:
            return False
    elif old_pawn_position[1]-2 == new_pawn_position[1]:
        if (old_pawn_position[0], old_pawn_position[1]-1) in walls[0] or (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] or (old_pawn_position[0], old_pawn_position[1]-2) in walls[0] or (old_pawn_position[0]-1, old_pawn_position[1]-2) in walls[0]:
            return False
    elif old_pawn_position[1]+2 == new_pawn_position[1]:
        if (old_pawn_position[0], old_pawn_position[1]) in walls[0] or (old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] or (old_pawn_position[0], old_pawn_position[1]+1) in walls[0] or (old_pawn_position[0]-1, old_pawn_position[1]+1) in walls[0]:
            return False
    elif old_pawn_position[0]-1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] or \
                (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1] or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1]) or \
                    ((old_pawn_position[0]-2, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]-2) in walls[1]):
                return False
        elif\
                ((old_pawn_position[0], old_pawn_position[1]) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[1]) or \
                ((old_pawn_position[0]-2, old_pawn_position[1]) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]+1) in walls[1]) or \
                (old_pawn_position[0]-1, old_pawn_position[1]) in walls[0] or \
            (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1]:
            return False
    elif old_pawn_position[0]+1 == new_pawn_position[0]:
        if old_pawn_position[1]-1 == new_pawn_position[1]:
            if\
                (old_pawn_position[0], old_pawn_position[1]-1) in walls[0] or \
                (old_pawn_position[0], old_pawn_position[1]-1) in walls[1] or \
                ((old_pawn_position[0]-1, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0], old_pawn_position[1]) in walls[1]) or \
                    ((old_pawn_position[0]+1, old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0], old_pawn_position[1]-2) in walls[1]):
                return False
        else:
            if\
                (old_pawn_position[0], old_pawn_position[1]) in walls[0] or \
                (old_pawn_position[0], old_pawn_position[1]) in walls[1] or \
                ((old_pawn_position[0], old_pawn_position[1]-1) in walls[0] and (old_pawn_position[0]-1, old_pawn_position[1]) in walls[1]) or \
                    ((old_pawn_position[0]+1, old_pawn_position[1]) in walls[0] and (old_pawn_position[0], old_pawn_position[1]+1) in walls[1]):
                return False
    return True


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


# sto manja to bolja
def h_calculate_raw(next_pos: tuple[int, int], dest_pos: tuple[int, int]) -> int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])


def h_calculate_optimized(dimensions: tuple[int, int], next_pos: tuple[int, int], dest_pos: tuple[int, int], heat_map: dict[tuple[int, int], int]) -> int:
    half_height = (dimensions[0]-1)/2
    # +heat_map[generate_next_moves]#vrv neki faktor za heat map# treba inverzna logika
    real = h_calculate_raw(next_pos, dest_pos)
    pom = (half_height-next_pos[0] if half_height >=
           next_pos[0] else next_pos[0]-half_height)
    rez = real-pom
    return rez


# def find_path(dimensions: tuple[int, int], walls[0]: list[tuple[int, int]], walls[1]: list[tuple[int, int]], pawn_pos: tuple[int, int], dest_pos: tuple[tuple[int, int], tuple[int, int]], heat_map: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
#     return(find_path_to_one(dimensions, walls[0], walls[1], pawn_pos, dest_pos[0], heat_map), find_path_to_one(dimensions, walls[0], walls[1], pawn_pos, dest_pos[0], heat_map))


# def find_path_to_one(dimensions: tuple[int, int], walls[0]: list[tuple[int, int]], walls[1]: list[tuple[int, int]], pawn_pos: tuple[int, int], dest_pos: tuple[int, int], heat_map: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
#     # if start[0]<0 or start[0]>5 or end[0]<0 or end[0]>5 or start[1]<0 or start[1]>5 or end[1]<0 or end[1]>5:
#     #     return "Losi parametri"
#     # if start[0]==end[0] and start[1]==end[1]:
#     #     return []
#     found_end = False
#     open_set = set([pawn_pos])
#     closed_set = set()
#     g = {}
#     prev_nodes = {}
#     g[pawn_pos] = 0
#     prev_nodes[pawn_pos] = None
#     while len(open_set) > 0 and (not found_end):
#         node = None
#         for next_node in open_set:
#             if node is None or g[next_node] + h_calculate_optimized(dimensions, next_node, dest_pos, heat_map) < g[node] + h_calculate_optimized(dimensions, next_node, dest_pos, heat_map):
#                 node = next_node
#         if node == dest_pos:
#             found_end = True
#             break
#         # print(node,end="")
#         for m in generate_next_moves(dimensions, walls[0], walls[1], node, dest_pos):
#             cost = h_calculate_optimized(dimensions, m, dest_pos, heat_map)
#             if m not in open_set and m not in closed_set:
#                 open_set.add(m)
#                 prev_nodes[m] = node
#                 g[m] = g[node] + cost
#             elif m not in closed_set and g[m] > g[node] + cost:
#                 g[m] = g[node] + cost
#                 prev_nodes[m] = node
#         open_set.remove(node)
#         closed_set.add(node)
#     path = []
#     if found_end:
#         prev = dest_pos
#         while prev_nodes[prev] is not None:
#             path.append(prev)
#             prev = prev_nodes[prev]
#         path.append(pawn_pos)
#         path.reverse()
#     return path


# def generate_next_moves(table_size: tuple[int, int], walls[0]: list[tuple[int, int]], walls[1]: list[tuple[int, int]], pawn_position: tuple[int, int], destination_position: tuple[int, int]) -> list[tuple[int, int]]:
#     # == 2
#     if abs(destination_position[0] - pawn_position[0]) + abs(destination_position[1] - pawn_position[1]) == 1 and is_pawn_move_valid(walls[0], walls[1], table_size, pawn_position, destination_position) == True:
#         return[destination_position]
#     return list(filter(lambda x: is_pawn_move_valid(walls[0], walls[1], table_size, pawn_position, x), map(lambda x: (pawn_position[0] + x[0], pawn_position[1] + x[1]), [(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0)])))
