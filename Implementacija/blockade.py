from moves import is_game_end, move_player
from utility import int_to_table_coordinate
from view import read_table_size, read_wall_count, read_first_player, read_start_positions, resize_terminal, show_end_screen, show_start_screen, show_table


def blockade() -> bool:
    resize_terminal(27, 80)
    show_start_screen()
    table_size = read_table_size()

    number_of_x_vertical_walls = read_wall_count()
    number_of_x_horizontal_walls = number_of_x_vertical_walls
    number_of_o_vertical_walls = number_of_x_vertical_walls
    number_of_o_horizontal_walls = number_of_x_vertical_walls

    computer_on_move = read_first_player()

    start_positions = read_start_positions(table_size[0], table_size[1])
    start_positions_o = [start_positions[1][0], start_positions[1][1]]
    start_positions_x = [start_positions[0][0], start_positions[0][1]]

    pawn_positions = start_positions
    del start_positions

    vertical_walls = list[tuple[int, int]]()
    horizontal_walls = list[tuple[int, int]]()
    vertical_walls.append((5,5))
    horizontal_walls.append((2,2))
    heat_map = dict[tuple[int, int], int]()
    for row in range(table_size[0]):
        key = int_to_table_coordinate(row)
        for column in range(table_size[1]):
            heat_map[key + int_to_table_coordinate(column)] = 0

    game_ended = False
    resize_terminal(2 * table_size[0] + 10, 4 * table_size[1] + 9)
    show_table(table_size[0], table_size[1], vertical_walls, horizontal_walls,
               pawn_positions[0][0], pawn_positions[0][1], pawn_positions[1][0], pawn_positions[1][1], start_positions_x, start_positions_o)

    while not game_ended:
        if(computer_on_move):
            computer_on_move = False

        else:
          #  pawn_positions = (((1, 1), (2, 2)), ((9, 9), start_positions_x[0]))
            c = int(input())
            d = int(input())

            pawn_positions = ((move_player(vertical_walls, horizontal_walls,
                                           pawn_positions[0][0], pawn_positions[1][0], pawn_positions[1][1], table_size[0], table_size[1], pawn_positions[0][0][0] + c, pawn_positions[0][0][1] + d), (4, 4)), ((3, 5), (4, 5)))
            computer_on_move = True

        show_table(table_size[0], table_size[1], vertical_walls, horizontal_walls,
                   pawn_positions[0][0], pawn_positions[0][1], pawn_positions[1][0], pawn_positions[1][1], start_positions_x, start_positions_o)

        game_ended = is_game_end(pawn_positions[0][0], pawn_positions[0][1], pawn_positions[1][0],
                                 pawn_positions[1][1], start_positions_x, start_positions_o)

    return show_end_screen(computer_on_move)
