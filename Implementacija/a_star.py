from Implementacija.moves import is_pawn_move_valid


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


def find_path(dimensions: tuple[int, int], vertical_walls: list[tuple[int, int]], horizontal_walls: list[tuple[int, int]], pawn_pos: tuple[int, int], dest_pos: tuple[tuple[int, int], tuple[int, int]], heat_map: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    return(find_path_to_one(dimensions, vertical_walls, horizontal_walls, pawn_pos, dest_pos[0], heat_map), find_path_to_one(dimensions, vertical_walls, horizontal_walls, pawn_pos, dest_pos[0], heat_map))


def find_path_to_one(dimensions: tuple[int, int], vertical_walls: list[tuple[int, int]], horizontal_walls: list[tuple[int, int]], pawn_pos: tuple[int, int], dest_pos: tuple[int, int], heat_map: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    # if start[0]<0 or start[0]>5 or end[0]<0 or end[0]>5 or start[1]<0 or start[1]>5 or end[1]<0 or end[1]>5:
    #     return "Losi parametri"
    # if start[0]==end[0] and start[1]==end[1]:
    #     return []
    found_end = False
    open_set = set([pawn_pos])
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[pawn_pos] = 0
    prev_nodes[pawn_pos] = None
    while len(open_set) > 0 and (not found_end):
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + h_calculate_optimized(dimensions, next_node, dest_pos, heat_map) < g[node] + h_calculate_optimized(dimensions, next_node, dest_pos, heat_map):
                node = next_node
        if node == dest_pos:
            found_end = True
            break
        # print(node,end="")
        for m in generate_next_moves(dimensions, vertical_walls, horizontal_walls, node, dest_pos):
            cost = h_calculate_optimized(dimensions, m, dest_pos, heat_map)
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
        prev = dest_pos
        while prev_nodes[prev] is not None:
            path.append(prev)
            prev = prev_nodes[prev]
        path.append(pawn_pos)
        path.reverse()
    return path


def generate_next_moves(table_size: tuple[int, int], vertical_walls: list[tuple[int, int]], horizontal_walls: list[tuple[int, int]], pawn_position: tuple[int, int], destination_position: tuple[int, int]) -> list[tuple[int, int]]:
    # == 2
    if abs(destination_position[0] - pawn_position[0]) + abs(destination_position[1] - pawn_position[1]) == 1 and is_pawn_move_valid(vertical_walls, horizontal_walls, table_size, pawn_position, destination_position) == True:
        return[destination_position]
    return list(filter(lambda x: is_pawn_move_valid(vertical_walls, horizontal_walls, table_size, pawn_position, x), map(lambda x: (pawn_position[0] + x[0], pawn_position[1] + x[1]), [(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0)])))
