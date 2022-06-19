
from game import Game
from cli_display import CLIDisplay


def main():
    game: Game = Game()
    game_display: CLIDisplay = CLIDisplay()

    while not game.game_over:
        game_display.draw(game)


if __name__ == "__main__":
    main()
