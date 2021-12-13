from blockade import blockade
from view import show_start_screen


def main():
    show_start_screen()
    gameLoop = blockade()
    while gameLoop:
        gameLoop = blockade()