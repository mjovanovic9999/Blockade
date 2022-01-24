from frozendict import frozendict
from min_max import min_max
from moves import generate_border_connection_points, is_game_end, update_wall_connection_points
from path_finding import find_path
from view import read_game_mode, read_move, read_table_size, read_wall_count, read_first_player, read_start_positions, resize_terminal, show_end_screen, show_start_screen, show_table
import constants



def blockade() -> bool:
    resize_terminal(30, 90)
    show_start_screen()

    table_size = read_table_size()

    number_of_walls = read_wall_count()

    start_positions = read_start_positions(table_size)

    pawn_positions = start_positions

    walls = ((), ())

    wall_connection_points = generate_border_connection_points(table_size)

    heat_map = dict[tuple[int, int], int]()
    for row in range(table_size[0]):
        for column in range(table_size[1]):
            heat_map[(row, column)] = 0

    
    x_to_move = True
    computer_is_x = True
    game_mode = multiplayer
    if read_game_mode():
        computer_is_x = read_first_player()
        game_mode = singleplayer

    resize_terminal(9999, 4 * table_size[1] + 12)
    show_table(table_size, walls,
               pawn_positions, start_positions)

    game_ended = False
    while not game_ended:
        pawn_positions, walls, number_of_walls, wall_connection_points = game_mode(
            pawn_positions, start_positions, walls, number_of_walls, table_size, x_to_move, wall_connection_points, computer_is_x)

        x_to_move = not x_to_move
        show_table(table_size, walls,
                   pawn_positions, start_positions)

        game_ended = is_game_end(pawn_positions, start_positions)

    return show_end_screen(x_to_move, game_mode == multiplayer)


def multiplayer(pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
                number_of_walls: tuple[tuple[int, int], tuple[int, int]],
                table_size: tuple[int, int],
                x_to_move: bool,
                connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
                _) -> tuple[tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]], tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]], tuple[tuple[int, int], tuple[int, int]]]:

    return read_move(pawn_positions, start_positions, walls, number_of_walls, table_size, x_to_move, connection_points)


def singleplayer(pawn_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                 start_positions: tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]],
                 walls: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
                 number_of_walls: tuple[tuple[int, int], tuple[int, int]],
                 table_size: tuple[int, int],
                 x_to_move: bool,
                 connection_points: frozendict[tuple[int, int], tuple[tuple[int, int], ...]],
                 computer_is_x:bool
                 ) -> tuple[tuple[tuple[tuple[int, int], tuple[int, int]], tuple[tuple[int, int], tuple[int, int]]], tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]], tuple[tuple[int, int], tuple[int, int]]]:
    if x_to_move == computer_is_x:
        print("Computer's turn:")
        min_max_state = min_max(pawn_positions,
                                start_positions,
                                walls, number_of_walls,
                                table_size,
                                {},
                                connection_points,
                                2,
                                not computer_is_x,
                                constants.MIN_VALUE,
                                constants.MAX_VALUE)
        
        return (min_max_state[-4], min_max_state[-3], min_max_state[-2], min_max_state[-9])
    return read_move(pawn_positions, start_positions, walls, number_of_walls, table_size, x_to_move, connection_points,False)
