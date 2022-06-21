import sys
import os
from game import Game
from cli_display import CLIDisplay


def main(skip_intro: bool = False):
    game: Game = Game()
    game_display: CLIDisplay = CLIDisplay(os.path.realpath(__file__))

    game_display.intro_screen(skip_intro)

    while not game.game_over:
        game_display.draw(game)


if __name__ == "__main__":
    skip_intro: bool = False
    if len(sys.argv) == 2:
        skip_intro = bool(sys.argv[1])

    main(skip_intro)
