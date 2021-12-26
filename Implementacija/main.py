from blockade import blockade
from view import clear_console, show_start_screen


def main():
    while blockade():
        clear_console()

main()