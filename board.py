from dataclasses import dataclass


@dataclass(slots=True)
class BoardSquare():
    column: int
    row: int
    is_red: bool | None
    is_part_of_four: bool = False

    def add_piece_to_board(self, is_red: bool) -> None:
        self.is_red = is_red

    def __lt__(self, other: 'BoardSquare') -> bool:
        return self.row < other.row
