from moves import *
from view import *
from utility import *
import time

clear_console()
#show_start_screen()


rowss=10
columnns=5
table=generate_empty_table(rowss, columnns)

table=add_horizontal_wall (table,rowss, columnns,2,4)
table=add_vertical_wall (table,rowss, columnns,1,2)
table=add_horizontal_wall (table,rowss, columnns,3,3)
# print(table)

table=add_pawn(table,rowss,columnns,1,1,True)
# print_table(table,column, rows)     

# time.sleep(1)
# clear_console()
# table=move_pawn(table,column,rows,1,1,8,8)

table=add_start_position(table,rowss,columnns,4,1,not False)

print_table(table,rowss, columnns)     
# print(show_end_screen())

# is_game_end((1,2,3))
print(place_wall(None,rowss,columnns,5,4,True))


#noviiiiiiiii222222222222