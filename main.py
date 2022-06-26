from game import Game
from cli_display import CLIDisplay


def main(skip_intro: bool = False):
    game: Game = Game()
    game_display: CLIDisplay = CLIDisplay()

    game_display.intro_screen(skip_intro)

    while True:
        game_display.draw(game)


if __name__ == "__main__":
    skip_intro: bool = False
    main(skip_intro)
