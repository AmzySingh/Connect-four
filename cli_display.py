import os
from game import Game
from custom_exceptions import ColumnFullException, ColumnNotExistsException


class _ColourText:

    @staticmethod
    def red(string: str) -> str:
        return f'\033[0;31;40m{string}\033[0;0m'

    @staticmethod
    def yellow(string: str) -> str:
        return f'\033[0;33;40m{string}\033[0;0m'

    @staticmethod
    def white(string: str) -> str:
        return f'\033[0;37;40m{string}\033[0;0m'

    @staticmethod
    def green(string: str) -> str:
        return f'\033[0;32;40m{string}\033[0;0m'


class CLIDisplay:
    def __init__(self) -> None:
        pass

    def _get_player_colour(self, game: Game) -> str:
        if game.red_turn:
            return _ColourText.red('Red')
        else:
            return _ColourText.yellow('Yellow')

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
                    return_str += _ColourText.white('[ ]')
                elif val.is_part_of_four and val.is_red:
                    return_str += _ColourText.white(
                        '[') + _ColourText.green('R') + _ColourText.white(']')
                elif val.is_part_of_four and not val.is_red:
                    return_str += _ColourText.white(
                        '[') + _ColourText.green('Y') + _ColourText.white(']')
                elif val.is_red:
                    return_str += _ColourText.white(
                        '[') + _ColourText.red('R') + _ColourText.white(']')
                else:
                    return_str += _ColourText.white(
                        '[') + _ColourText.yellow('Y') + _ColourText.white(']')

            return_str += '\n'

        print(return_str)

    def _user_input_col(self, game: Game) -> bool | None:
        correct_user_input: bool = False
        result_col: int = 0
        while not correct_user_input:
            question: str = f"""{self._get_player_colour(game)} player, select a column to add a piece into (type "exit" to exit): """
            result: str = input(question)
            if result == 'exit':
                game.game_over = True
                return False
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
            self._user_input_col(game)
        except ColumnFullException:
            print(f"Column {result_col} is full")
            self._user_input_col(game)

        return None

    def _game_over_msg(self, game: Game) -> None:
        print(
            f"The game is over, {self._get_player_colour(game)} player wins!!")

        print(f"{_ColourText.green('Green')} shows the winning line")

    def _tie_msg(self, game: Game) -> None:
        print("No spaces left, the game is a tie!")

    def _close_game(self, game: Game) -> None:
        user_close: str = input("""
Type "exit" to exit the game

Type "restart" to play again: """)
        if user_close == 'exit':
            game.game_over = True
        elif user_close == 'restart':
            game.reset_game()

        else:

            self.clear_console()
            self._close_game(game)

    @staticmethod
    def clear_console():
        command: str = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    def draw(self, game: Game) -> None:
        self.clear_console()
        self._display_turn(game)
        self._display_board_key(game)
        self._display_board(game)

        if not game.game_over:
            if self._user_input_col(game) is None:
                self.draw(game)

        elif not game.check_not_tie:
            self._tie_msg(game)
            self._close_game(game)
        else:
            self._game_over_msg(game)
            self._close_game(game)

    def intro_screen(self, skip_intro: bool, game: Game) -> None:
        if skip_intro:
            return
        self.clear_console()
        intro_msg: str = """Welcome to Amzy's Connect Four Game. 

The rules are simple, 2 colour pieces, select a column to drop a piece, first to make four in a row (horizonal/vertical/diagonal) wins

Type "start" to begin the game or "exit" to quit: """

        user_input: str = input(intro_msg)

        if user_input == 'exit':
            game.game_over = True

        elif user_input == 'start':
            pass
        else:
            self.clear_console()
            self.intro_screen(skip_intro, game)
