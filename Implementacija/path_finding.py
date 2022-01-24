from queue import LifoQueue

from frozendict import frozendict
import moves


# sto manja to bolja
def h_calculate_raw(next_pos: tuple[int, int], dest_pos: tuple[int, int]) -> int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])


# def h_calculate_optimized(dimensions: tuple[int, int], next_position: tuple[int, int], dest_pos: tuple[int, int], destination_quadrant: int, heat_map: dict[tuple[int, int], int]) -> int:
#     # +heat_map[generate_next_moves]#vrv neki faktor za heat map# treba inverzna logika
#     if next_position == dest_pos:
#          return -1000

#     next_position_quadrant = find_positions_quadrant(next_position, dimensions)
#     real = h_calculate_raw(next_position, dest_pos)

#     if destination_quadrant == 1:
#         if next_position_quadrant == 2:
#            return real + 100 * (next_position[0] - 1)
#         if next_position_quadrant == 3:
#             return real + 100 * (dimensions[0] - next_position[0])
#         if next_position_quadrant == 4:
#             return real + 100 * (dimensions[1] - next_position[1])
#         if next_position[0] <= dest_pos[0]:
#             if next_position[1] > dest_pos[1]:
#                 return real + 1000000
#             return real + 100 * (next_position[0] - 1)
#         if next_position[1] >= dest_pos[1]:
#             if next_position[0] < dest_pos[0]:
#                 return real + 1000000
#             return real + 100 * (dimensions[1] - next_position[1])

#     if destination_quadrant == 4:
#         if next_position_quadrant == 2:
#             return real + 100 * (next_position[0] - 1)
#         if next_position_quadrant == 3:
#             return real + 100 * (dimensions[0] - next_position[0])
#         if next_position_quadrant == 1:
#             return real + 100 * (dimensions[1] - next_position[1])
#         if next_position[0] >= dest_pos[0]:
#             if next_position[1] > dest_pos[1]:
#                 return real + 1000000
#             return real + 100 * (dimensions[0] - next_position[0])
#         if next_position[1] >= dest_pos[1]:
#             if next_position[0] > dest_pos[0]:
#                 return real + 1000000
#             return real + 100 * (dimensions[1] - next_position[1])

#     if destination_quadrant == 3:
#         if next_position_quadrant == 1:
#             return real + 100 * (next_position[0] - 1)
#         if next_position_quadrant == 2:
#             return real + 100 * (next_position[1] - 1)
#         if next_position_quadrant == 4:
#             return real + 100 * (dimensions[0] - next_position[0])
#         if next_position[0] >= dest_pos[0]:
#             if next_position[1] < dest_pos[1]:
#                 return real + 1000000
#             return real + 100 * (dimensions[0] - next_position[0])
#         if next_position[1] <= dest_pos[1]:
#             if next_position[0] > dest_pos[0]:
#                 return real + 1000000
#             return real + 100 * (next_position[1] - 1)

#     if destination_quadrant == 2:
#         if next_position_quadrant == 1:
#             return real + 100 * (next_position[0] - 1)
#         if next_position_quadrant == 3:
#             return real + 100 * (next_position[1] - 1)
#         if next_position_quadrant == 4:
#             return real + 100 * (dimensions[0] - next_position[0])
#         if next_position[0] <= dest_pos[0]:
#             if next_position[1] < dest_pos[1]:
#                 return real + 1000000
#             return real + 100 * (next_position[0] - 1)
#         if next_position[1] <= dest_pos[1]:
#             if next_position[0] < dest_pos[0]:
#                 return real + 1000000
#             return real + 100 * (next_position[1] - 1)

#     return real + 1000000

# def find_positions_quadrant(position: tuple[int, int], table_size: tuple[int, int]) -> int:
#     upper_half = position[0] <= table_size[0]/2
#     right_half = position[1] >= table_size[1]/2

#     if upper_half:
#         if right_half:
#             return 1
#         return 2
#     if right_half:
#         return 4
#     return 3

def find_path(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,
    selected_destination_index: int,
    heat_map: dict[tuple[int, int], int]
):
    return(tuple(a_star(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, start_positions[not selected_player_index][selected_destination_index], heat_map)))

# najoptimalnije na zatvaranje da se proveri da l je neka putanja presecena; ako jeste opet se poziva


def a_star(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,
    destination_position: tuple[int, int],
    heat_map: dict[tuple[int, int], int]
) -> list[tuple[int, int]]:
    pawn_position = current_pawns_positions[selected_player_index][selected_pawn_index]

    found_end = False
    open_set = set([pawn_position])
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[pawn_position] = 0
    prev_nodes[pawn_position] = None
    while len(open_set) > 0 and (not found_end):
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + h_calculate_raw(node, destination_position) < g[node] + h_calculate_raw(node, destination_position):
                node = next_node
        if node == destination_position:
            found_end = True
            break
        # print(node,end="")
        for m in generate_next_moves(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, node):
            cost = h_calculate_raw(node, destination_position)
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                prev_nodes[m] = node
                g[m] = g[node] + cost
            elif m not in closed_set and g[m] > g[node] + cost:
                g[m] = g[node] + cost
                prev_nodes[m] = node
        open_set.remove(node)
        closed_set.add(node)
    path = []
    if found_end:
        prev = destination_position
        while prev_nodes[prev] is not None:
            path.append(prev)
            prev = prev_nodes[prev]
        path.append(pawn_position)
        path.reverse()
    return path


# def find_path_to_one(
#     current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
#     start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
#     walls: tuple[tuple, tuple],
#     table_size: tuple[int, int],
#     selected_player_index: int,
#     selected_pawn_index: int,
#     destination_position: tuple[int, int],
#     heat_map: dict[tuple[int, int], int]
# ) -> list[tuple[int, int]]:
#     pawn_position = current_pawns_positions[selected_player_index][selected_pawn_index]

#     if pawn_position == destination_position:
#         path = list()
#         path.append(pawn_position)
#         return path

#     stack_nodes = LifoQueue()
#     visited = set()
#     prev_nodes = dict()
#     prev_nodes[pawn_position] = None
#     visited.add(pawn_position)
#     stack_nodes.put(pawn_position)
#     found_dest = False
#     destination_quadrant = find_positions_quadrant(destination_position, table_size)

#     while (not found_dest) and (not stack_nodes.empty()):
#         node = stack_nodes.get()
#         a = sorted(generate_next_moves(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, node), key = lambda next_move: h_calculate_optimized(table_size, next_move, destination_position, destination_quadrant, heat_map), reverse=True)
#         for dest in sorted(generate_next_moves(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, node), key = lambda next_move: h_calculate_optimized(table_size, next_move, destination_position, destination_quadrant, heat_map), reverse=True):
#             if dest not in visited:
#                 prev_nodes[dest] = node
#                 if dest == destination_position:
#                     found_dest = True
#                     break
#                 visited.add(dest)
#                 stack_nodes.put(dest)
#     path = list()
#     if found_dest:
#         path.append(destination_position)
#         prev = prev_nodes[destination_position]
#         while prev is not None:
#             path.append(prev)
#             prev = prev_nodes[prev]
#         path.reverse()
#     return path


def generate_next_moves(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    # ovo je bio destination
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,
    current_position: tuple[int, int]
) -> list[tuple[int, int]]:
    return list(filter(lambda x: moves.is_pawn_move_valid(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, current_position, x), map(lambda x: (current_position[0] + x[0], current_position[1] + x[1]), [(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0), (-1, 0), (1, 0), (0, -1), (0, 1)])))


def do_walls_make_polygon(connection_points: dict[tuple[int, int], tuple[tuple[int, int], ...]],
                          start: tuple[int, int],
                          end: tuple[int, int]) -> bool:

    stack_nodes = LifoQueue(len(connection_points))
    visited = set()
    prev_nodes = dict()
    prev_nodes[start] = None
    visited.add(start)
    stack_nodes.put(start)

    while not stack_nodes.empty():
        node = stack_nodes.get()
        for dest in connection_points[node]:
            if dest not in visited:
                prev_nodes[dest] = node
                if dest == end:
                    return True
                else:
                    visited.add(dest)
                    stack_nodes.put(dest)

    return False
