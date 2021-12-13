from blockade import blockade
from view import clear_console, show_start_screen


def main():
    show_start_screen()
    while blockade():
        clear_console()

main()