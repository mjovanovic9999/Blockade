from moves import is_pawn_move_valid


# sto manja to bolja
def h_calculate_raw(next_pos: tuple[int, int], dest_pos: tuple[int, int]) -> int:
    return abs(next_pos[0]-dest_pos[0])+abs(next_pos[1]-dest_pos[1])


def h_calculate_optimized(dimensions: tuple[int, int], next_position: tuple[int, int], dest_pos: tuple[int, int], heat_map: dict[tuple[int, int], int]) -> int:
    half_height = (dimensions[0]-1)/2
    # +heat_map[generate_next_moves]#vrv neki faktor za heat map# treba inverzna logika
    real = h_calculate_raw(next_position, dest_pos)
    pom = (half_height-next_position[0] if half_height >=
           next_position[0] else next_position[0]-half_height)
    rez = real-pom*real/2.5#bilo je /2
    return rez

#mozda optimizacija za gore dole src i dst


def find_path(dimensions: tuple[int, int], vertical_walls: list[tuple[int, int]], horizontal_walls: list[tuple[int, int]], pawn_pos: tuple[int, int], dest_pos: tuple[tuple[int, int], tuple[int, int]], heat_map: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    return(find_path_to_one(dimensions, vertical_walls, horizontal_walls, pawn_pos, dest_pos[0], heat_map), find_path_to_one(dimensions, vertical_walls, horizontal_walls, pawn_pos, dest_pos[0], heat_map))

#najoptimalnije na zatvaranje da se proveri da l je neka putanja presecena; ako jeste opet se poziva
def find_path_to_one(
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
    walls: tuple[tuple, tuple],
    table_size: tuple[int, int],
    selected_player_index: int,
    selected_pawn_index: int,
    destination_position: tuple[int, int],######## koji je dest iz start positions da se izabere!!!
    heat_map: dict[tuple[int, int], int]
    ) -> list[tuple[int, int]]:
    #[] -> ako ne postoji putanja
    #[(x,y)] -> ako je src i dst isto polje
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
            if node is None or g[next_node] + h_calculate_optimized(table_size, next_node, destination_position, heat_map) < g[node] + h_calculate_optimized(table_size, next_node, destination_position, heat_map):
                node = next_node
        if node == destination_position:
            found_end = True
            break
        # print(node,end="")
        for m in generate_next_moves(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index):
            cost = h_calculate_optimized(table_size, m, destination_position, heat_map)
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
    current_pawns_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],#
    start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],#ovo je bio destination
    walls: tuple[tuple, tuple],#
    table_size: tuple[int, int],#
    selected_player_index: int,#zbog prvo
    selected_pawn_index: int, #zbog prvo
    ) -> list[tuple[int, int]]:
    # == 2
    pawn_position = current_pawns_positions[selected_player_index][selected_pawn_index]
    return list(filter(lambda x: is_pawn_move_valid(current_pawns_positions, start_positions, walls, table_size, selected_player_index, selected_pawn_index, x), map(lambda x: (pawn_position[0] + x[0], pawn_position[1] + x[1]), [(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0), (-1, 0),(1, 0),(0, -1),(0, 1)])))


#to delete: ptrptr
# print(find_path_to_one((6,6),(((0,2),(2,2)),(1 ,0)),(2,4),{}))
# print('\n')

# for i in range(0,6):
#     for j in range(0,6):
#         print("("+str(i)+","+str(j)+")", end=" ")
#     print('\n')