import numpy as np
import ipdb


board_width = 4
# pieces_shapes = [[(0, 0)] for _ in range(board_width**2)]
pieces_shapes = [[(0, 0), (0, 1), (1, 0), (2, 0)] for _ in range(4)]


class Piece:
    def _move_to_top_left_corner(matr):
        while not np.any(matr[0, :]):
            matr = np.roll(matr, -1, axis=0)
        while not np.any(matr[:, 0]):
            matr = np.roll(matr, -1, axis=1)
        return matr

    def _gen_all_translations(matr):
        all_translations = []
        for r in range(board_width):
            for c in range(board_width):
                m = np.roll(matr, (r, c), axis=(0, 1))
                all_translations.append(m)
                if np.any(m[:, -1]):
                    break
            if np.any(m[-1, :]):
                break
        return all_translations

    def _gen_all_placements(matr):
        all_placements = []
        for n_rot in range(4):
            matr_rot = np.rot90(matr, n_rot)
            matr_rot = Piece._move_to_top_left_corner(matr_rot)
            all_placements.extend(Piece._gen_all_translations(matr_rot))

        # Remove duplicates (due to symmetry)
        all_placements = np.unique(all_placements, axis=0)

        return all_placements

    def __init__(self, piece_number, pos_tuples) -> None:
        self.piece_number = piece_number
        matrix = np.zeros([board_width, board_width])
        for tuple in pos_tuples:
            matrix[tuple[0], tuple[1]] = piece_number
        self._matrix = matrix
        self._all_placements = Piece._gen_all_placements(self._matrix)

    def placements_covering(self, row, col):
        return self._all_placements[self._all_placements[:, row, col] > 0]


class Board:
    @classmethod
    def empty(cls):
        return cls(set(), np.zeros([board_width, board_width]))

    @classmethod
    def add_piece(cls, board, piece_number, placement):
        return cls(board.pieces.union([piece_number]), board._matrix + placement)

    def __init__(self, pieces, matrix) -> None:
        self.pieces = pieces
        self._matrix = matrix

    def first_empty_slot(self):
        for row in range(board_width):
            for col in range(board_width):
                if self._matrix[row, col] == 0:
                    return row, col

    def contains_piece(self, piece_number):
        return piece_number in self.pieces

    def would_cause_overlap(self, placement):
        return np.any(np.logical_and(self._matrix, placement))


def precompute_next_placements(pieces: list[Piece]):
    placements = {}
    for row in range(board_width):
        placements[row] = {}
        for col in range(board_width):
            placements[row][col] = {}
            for i, piece in enumerate(pieces):
                placements[row][col][piece.piece_number] = piece.placements_covering(
                    row, col
                )
    return placements


def main():

    pieces = [Piece(i + 1, piece_shape) for i, piece_shape in enumerate(pieces_shapes)]
    next_placements = precompute_next_placements(pieces)

    # Put an empty board on the stack
    stack = [Board.empty()]

    while stack:

        # Take the first board from the stack and find the first empty slot
        board = stack.pop()
        print(f"stack len: {len(stack)}. Pieces on board: {board.pieces}")
        if len(board.pieces) == len(pieces):
            print("Found a solution!")
            print(board._matrix)
            exit()
        row, col = board.first_empty_slot()
        print(f"First empty row: {row}. col: {col}.")

        for piece_number, piece_placements in next_placements[row][col].items():
            if not board.contains_piece(piece_number):
                for piece_placement in piece_placements:
                    if not board.would_cause_overlap(piece_placement):
                        new_board = Board.add_piece(
                            board, piece_number, piece_placement
                        )
                        stack.append(new_board)


# repeat:
#   take the first board from the stack
#   find the first empty slot
#   for every piece/rotation/position that covers that slot
#       if the piece is not already placed
#          if there are no overlaps (optimisation: and a feasible solution cannot be ruled out)
#               place the piece
#               put board on the stack

if __name__ == "__main__":
    main()
