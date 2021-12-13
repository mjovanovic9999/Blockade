from moves import is_game_end
from utility import int_to_table_coordinate
from view import read_table_size, read_wall_count, read_first_player, read_start_positions, show_end_screen


def blockade() -> bool:
    table_size = read_table_size()
    number_of_walls = read_wall_count()
    computer_on_move = read_first_player()
    start_positions = read_start_positions(table_size[0], table_size[1])
    pawn_positions = start_positions
    vertical_walls = {}
    horizontal_walls = {}
    heat_map = {}

    winner = 0


    while winner == 0:
        pawn_x1 = pawn_positions[0][0]
        pawn_x2 = pawn_positions[0][1]
        start_positions_x = [start_positions[0][0], start_positions[0][1]]

        pawn_o1 = pawn_positions[1][0]
        pawn_o2 = pawn_positions[1][1]
        start_positions_o = [start_positions[1][0], start_positions[1][1]]
        
        winner = is_game_end(pawn_x1, pawn_x2, pawn_o1, pawn_o2, start_positions_x, start_positions_o)
        
        if input("A") == "A":
            winner = 1

    return show_end_screen(winner)