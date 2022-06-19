from game import Game
from os import system
from custom_exceptions import ColumnFullException, ColumnNotExistsException


class ColourText:

    @staticmethod
    def red(string: str) -> str:
        return f'\033[0;31;40m{string}\033[0;0m'

    @staticmethod
    def yellow(string: str) -> str:
        return f'\033[0;33;40m{string}\033[0;0m'

    @staticmethod
    def white(string: str) -> str:
        return f'\033[0;37;40m{string}\033[0;0m'


class CLIDisplay:
    def __init__(self) -> None:
        pass

    def _get_player_colour(self, game: Game) -> str:
        if game.red_turn:
            return ColourText.red('Red')
        else:
            return ColourText.yellow('Yellow')

    def _display_turn(self, game: Game) -> None:
        persons_turn: str = self._get_player_colour(game)

        print(f"It's {persons_turn} players turn!\n")

    def _display_board_key(self, game: Game) -> None:
        print(' 1  2  3  4  5  6  7')

    def _display_board(self, game: Game) -> None:
        return_str: str = ''

        for row in range(1, game.board_height+1):
            current_row: Game.BS = []

            for piece in game.board:
                if piece.row == row:
                    current_row.append(piece)

            sorted(current_row, key=lambda self: self.column)
            for val in current_row:
                if val.is_red is None:
                    return_str += ColourText.white('[ ]')
                elif val.is_red == True:
                    return_str += ColourText.white(
                        '[') + ColourText.red('R') + ColourText.white(']')
                else:
                    return_str += ColourText.white(
                        '[') + ColourText.yellow('Y') + ColourText.white(']')

            return_str += '\n'

        print(return_str)

    def user_input_col(self, game: Game) -> None:
        correct_user_input: bool = False
        result_col: int = 0
        while not correct_user_input:
            question: str = f"{self._get_player_colour(game)} player, select a column to add a piece into (type 'exit' to exit): "
            result: str = input(question)
            if result == 'exit':
                exit()
            try:
                result_col = int(result)
            except ValueError:
                print(f"{result} is not a valid number! Please try again")
                continue

            correct_user_input = True

        try:
            game.take_turn(result_col)
        except ColumnNotExistsException:
            print(f"Column {result_col} does not exist")
            self.user_input_col(game)
        except ColumnFullException:
            print(f"Column {result_col} is full")
            self.user_input_col(game)

    def game_over_msg(self, game: Game) -> None:
        print(
            f"The game is over, {self._get_player_colour(game)} player wins!!")

    def tie_msg(self, game: Game) -> None:
        print("No spaces left, the game is a tie!")

    def close_game(self) -> None:
        user_close: str = input("Type 'exit' to exit the game: ")
        if user_close == 'exit':
            exit()
        else:
            self.close_game()

    def draw(self, game: Game) -> None:
        system('cls')
        self._display_turn(game)
        self._display_board_key(game)
        self._display_board(game)

        if not game.game_over:
            self.user_input_col(game)
            self.draw(game)

        elif not game.check_not_tie:
            self.tie_msg(game)
            self.close_game()
        else:
            self.game_over_msg(game)
            self.close_game()
