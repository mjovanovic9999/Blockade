from queue import LifoQueue

from frozendict import frozendict
import moves


# sto manja to bolja
def h_calculate_raw(next_pos: tuple[int, int], dest_pos: tuple[int, int]) -> int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])


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
