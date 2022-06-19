from board import BoardSquare
from typing import TypeAlias
from custom_exceptions import ColumnFullException, ColumnNotExistsException, LeavingBoardException, PieceNotFound

width: int = 7
height: int = 6


class Game:
    BS: TypeAlias = list[BoardSquare]
    Vector: TypeAlias = tuple[int, int]

    def __init__(self, board_width: int = width, board_height: int = height):
        self.board_width = board_width
        self.board_height = board_height

        self.red_turn: bool = True
        self.game_over: bool = False

        self.board: Game.BS = []

        for i in range(board_width):
            for j in range(board_height):
                self.board.append(BoardSquare(i+1, j+1, None))

    def get_empty_pieces_per_column(self, col_num: int) -> BS:
        return_value: Game.BS = []
        for piece in self.board:
            if piece.column == col_num and piece.is_red is None:
                return_value.append(piece)

        return return_value

    def get_empty_pieces_per_row(self, row_num: int) -> BS:
        return_value: Game.BS = []
        for piece in self.board:
            if piece.row == row_num and piece.is_red is None:
                return_value.append(piece)

        return return_value

    def get_piece_from_coords(self, vec: Vector) -> BoardSquare:
        col, row = vec
        if col > self.board_width:
            raise LeavingBoardException(
                f'col {col} is out of range {self.board_width}')
        elif row > self.board_height:
            raise LeavingBoardException(
                f'row {row} is out of range {self.board_height}')

        for piece in self.board:
            if piece.column == col and piece.row == row:
                return piece
        else:
            raise PieceNotFound('Piece not found')

    def add_piece_to_col(self, col: int, is_red: bool) -> None:
        if col not in range(1, self.board_width+1):
            msg: str = f'Column {col} does not exist'
            raise ColumnNotExistsException(msg)
        items_col = self.get_empty_pieces_per_column(col)
        if len(items_col) == 0:
            msg = f'Column {col} is full'
            raise ColumnFullException(msg)
        piece_to_add_to = max(items_col)
        piece_to_add_to.add_piece_to_board(is_red)

    def take_turn(self, col: int) -> None:
        self.add_piece_to_col(col, is_red=self.red_turn)
        if self.check_four_in_a_row():
            return None
        self.red_turn = not self.red_turn

        if not self.check_not_tie:
            self.game_over = True

    def pieces_around_piece(self, current_square: BoardSquare) -> 'Game.BS':
        pieces_around: Game.BS = []
        if current_square.is_red is None:
            msg: str = f"{current_square} doesn't have a piece in it"
            raise ValueError(msg)

        for square in self.board:
            if current_square.row == square.row and current_square.column in [square.column+1, square.column-1] and current_square.is_red == square.is_red:
                pieces_around.append(square)
            elif current_square.row in [square.row+1, square.row-1] and current_square.column in [square.column, square.column-1, square.column+1] and current_square.is_red == square.is_red:
                pieces_around.append(square)

        return pieces_around

    def get_direction_vector(self, current_square: BoardSquare, other_square: BoardSquare) -> Vector:
        return (other_square.column-current_square.column, other_square.row-current_square.row)

    def find_lenght_of_line(self, current_square: BoardSquare, other_square: BoardSquare) -> BS:
        movement_vector: Game.Vector = self.get_direction_vector(
            current_square, other_square)

        current_line: Game.BS = [current_square, other_square]

        while len(current_line) < 4:
            other_square_vector: Game.Vector = (
                other_square.column, other_square.row)
            new_coords: Game.Vector = self.add_coords_to_coords(
                other_square_vector, movement_vector)
            try:
                next_piece: BoardSquare = self.get_piece_from_coords(
                    new_coords)
            except LeavingBoardException:
                break
            except PieceNotFound:
                break

            if next_piece.is_red == other_square.is_red:
                other_square = next_piece
                current_line.append(other_square)
            else:
                break

        return current_line

    @staticmethod
    def add_coords_to_coords(start: Vector, move: Vector) -> Vector:
        return (start[0]+move[0], start[1]+move[1])

    def check_four_in_a_row(self) -> bool:
        for square in self.board:

            if square.is_red is not None:
                pieces_around: Game.BS = self.pieces_around_piece(square)
                for next_square in pieces_around:
                    current_line: Game.BS = self.find_lenght_of_line(
                        square, next_square)
                    if len(current_line) >= 4:
                        self.game_over = True
                        for square in current_line:
                            square.is_part_of_four = True
                        return True

        return False

    @property
    def check_not_tie(self) -> bool:
        for square in self.board:
            if square.is_red is None:
                return True
        else:
            return False
