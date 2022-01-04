
from moves import is_game_end, place_wall
from view import read_game_mode, read_move, read_table_size, read_wall_count, read_first_player, read_start_positions, resize_terminal, show_end_screen, show_start_screen, show_table


def blockade() -> bool:
    resize_terminal(30, 90)
    show_start_screen()
    table_size = read_table_size()

    number_of_walls = read_wall_count()

    start_positions = read_start_positions(table_size)

    pawn_positions = start_positions

    walls = ((),())
    heat_map = dict[tuple[int, int], int]()
    for row in range(table_size[0]):
        for column in range(table_size[1]):
            heat_map[(row, column)] = 0

    computer_or_x_to_move = True
    game_mode = multiplayer
    if read_game_mode():
        computer_or_x_to_move = read_first_player()
        game_mode = singleplayer

    resize_terminal(9999, 4 * table_size[1] + 12)
    show_table(table_size, walls,
               pawn_positions, start_positions)

    game_ended = False
    while not game_ended:
        pawn_positions, = game_mode(pawn_positions, start_positions, walls, number_of_walls , table_size, computer_or_x_to_move)

        computer_or_x_to_move = not computer_or_x_to_move
        show_table(table_size, walls,
                   pawn_positions, start_positions)

        game_ended = is_game_end(pawn_positions, start_positions)

    return show_end_screen(computer_or_x_to_move, game_mode == multiplayer)


def multiplayer(pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                walls: tuple[tuple, tuple],
                number_of_walls: tuple[tuple[int, int], tuple[int, int]],
                table_size: tuple[int, int],
                x_to_move: bool) -> tuple[tuple[int, int]]:

    return read_move(pawn_positions, start_positions, walls, number_of_walls, table_size, x_to_move)


def singleplayer(computer_to_move: bool) -> bool:
    pass
