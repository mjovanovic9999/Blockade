
from view import read_table_size, read_wall_count, read_first_player, read_start_positions, resize_terminal, show_end_screen, show_start_screen, show_table


def blockade() -> bool:
    resize_terminal(30, 90)
    show_start_screen()
    table_size = read_table_size()

    number_of_x_vertical_walls = read_wall_count()
    number_of_x_horizontal_walls = number_of_x_vertical_walls
    number_of_o_vertical_walls = number_of_x_vertical_walls
    number_of_o_horizontal_walls = number_of_x_vertical_walls

    start_positions = read_start_positions(table_size[0], table_size[1])

    pawn_positions = start_positions

    vertical_walls = list[tuple[int, int]]()
    horizontal_walls = list[tuple[int, int]]()

    heat_map = dict[tuple[int, int], int]()
    for row in range(table_size[0]):
        for column in range(table_size[1]):
            heat_map[(row, column)] = 0

    resize_terminal(2 * table_size[0] + 10, 4 * table_size[1] + 9)
    show_table(table_size[0], table_size[1], vertical_walls, horizontal_walls,
               pawn_positions[0][0], pawn_positions[0][1], pawn_positions[1][0], pawn_positions[1][1], start_positions[0], start_positions[1])
    computer_or_x_to_move = False
    game_ended = False
    input()
    # while not game_ended:
    #     next_move = ()

    #     pawn_positions = ((move_pawn(vertical_walls, horizontal_walls,
    #                                  pawn_positions[0][0], pawn_positions[1][0], pawn_positions[1][1], table_size[0], table_size[1], pawn_positions[0][0][0], pawn_positions[0][0][1]), (4, 4)), ((3, 5), (4, 5)))

    #     computer_or_x_to_move = not computer_or_x_to_move
    #     show_table(table_size[0], table_size[1], vertical_walls, horizontal_walls,
    #                pawn_positions[0][0], pawn_positions[0][1], pawn_positions[1][0], pawn_positions[1][1], start_positions[0], start_positions[1])

    #     game_ended = is_game_end(pawn_positions[0][0], pawn_positions[0][1], pawn_positions[1][0],
    #                              pawn_positions[1][1], start_positions[0], start_positions[1])

    return show_end_screen(computer_or_x_to_move, False)


def multiplayer(x_to_move: bool) -> bool:

    pass


def singleplayer() -> bool:
    pass
