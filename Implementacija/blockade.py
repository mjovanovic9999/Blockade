from utility import int_to_table_coordinate
from view import read_table_size, read_wall_count, read_first_player, read_start_positions


def blockade():
    return


def game_init():
    table_size = read_table_size()
    number_of_walls = read_wall_count()
    computer_plays_first = read_first_player()
    start_positions = read_start_positions(table_size[0], table_size[1])

    initial_state = dict()
    for i in range(table_size[1]):
        key = int_to_table_coordinate(i)

        for j in range(table_size[0]):
            key += int_to_table_coordinate(j)
            initial_state[key] = (0, 0, 0)

    #initial_state[start_positions[0][]]
    return (table_size, number_of_walls, computer_plays_first, start_positions)
