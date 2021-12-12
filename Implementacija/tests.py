from moves import is_game_end
from view import *
from utility import *
import time

clear_console()
#show_start_screen()


column=5
rows=5
table=generate_empty_table(column, rows)

table=add_horizontal_wall (table,column, rows,2,4)
table=add_vertical_wall (table,column, rows,1,2)
table=add_horizontal_wall (table,column, rows,3,3)
# print(table)

table=add_pawn(table,column,rows,1,1,True)
# print_table(table,column, rows)     

# time.sleep(1)
# clear_console()
# table=move_pawn(table,column,rows,1,1,8,8)

table=add_start_position(table,column,rows,3,3,not False)

print_table(table,column, rows)     
# print(show_end_screen())

# is_game_end((1,2,3))

print(int_to_row_coordinate(1))