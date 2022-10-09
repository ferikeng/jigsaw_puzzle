import numpy as np
import ipdb

board_width = 16
pieces_shapes = [
    # 1 Pink
    [(0, c) for c in range(9)]
    + [(1, c) for c in [3, 4, 5, 6]]
    + [(2, c) for c in [3, 6]],
    # 2 Purple
    [(r, c) for r in range(2) for c in range(6)]
    + [(2, c) for c in range(2, 6)]
    + [(3, 2), (3, 5)],
    # 3 Orange
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
    + [(r, c) for r in [3, 4] for c in [2, 3, 4]]
    + [(r, c) for r in [5, 6] for c in [2, 4]],
    # 4 Yellow
    [(0, c) for c in range(6)]
    + [(r, 5) for r in [1, 2, 3, 4]]
    + [(4, 4), (4, 3), (3, 3)],
    # 5 Light Blue
    [(0, 7)]
    + [(1, c) for c in range(8)]
    + [(2, c) for c in range(6)]
    + [(3, 3), (3, 5)],
    # 6 Purple
    [(r, c) for r in [0, 1] for c in range(5)] + [(2, 2), (2, 4)],
    # 7 Green
    [(0, c) for c in [3, 4, 5]]
    + [(1, c) for c in range(4)]
    + [(2, c) for c in [1, 2, 3, 4]]
    + [(3, c) for c in [1, 2, 4]],
    # 8 Pink
    [(0, c) for c in range(9)] + [(1, 4), (1, 6)],
    # 9 Green
    [(0, 1), (0, 4)] + [(1, c) for c in range(7)] + [(2, 0), (2, 2), (2, 4)],
    # 10 Blue
    [(r, c) for r in range(4) for c in range(3)] + [(4, 0), (5, 0), (5, 1)],
    # 11 Red
    [(0, 0), (0, 1), (1, 1), (3, 1), (3, 4)] + [(2, c) for c in range(1, 7)],
    # 12 Turqoise
    [(0, 2), (1, 2), (1, 3), (1, 4)]
    + [(2, c) for c in range(5)]
    + [(3, 4), (3, 5), (3, 6)],
    # 13 Light blue
    [(0, 4), (0, 5), (1, 5)]
    + [(2, c) for c in [0, 1, 3, 4, 5]]
    + [(3, c) for c in [1, 2, 3]],
    # 14 Yellow
    [(0, 0), (0, 1)]
    + [(1, c) for c in range(5)]
    + [(r, c) for r in [2, 3] for c in [0, 1, 2]],
    # 15 Teal
    [(0, c) for c in range(7)]
    + [(1, c) for c in [0, 2, 3, 4, 5, 6]]
    + [(2, 2), (2, 6)],
    # 16 Orange
    [(0, 1), (0, 2)]
    + [(1, c) for c in range(4)]
    + [(2, c) for c in range(5)]
    + [(3, 2), (3, 4)],
    # 17 Purple
    [(r, c) for r in range(0, 2) for c in range(1, 8)]
    + [(2, c) for c in [0, 1, 3, 7]]
    + [(3, c) for c in [3, 7]],
    # 18 Yellow
    [(0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2)],
    # 19 Turqoise
    [(0, 2)] + [(1, c) for c in range(5)] + [(2, c) for c in range(4)],
]


# board_width = 4
# pieces_shapes = [[(0, 0)] for _ in range(board_width**2)]
# pieces_shapes = [[(0, 0), (0, 1), (1, 0), (2, 0)] for _ in range(4)]


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
        return cls(list(), np.zeros([board_width, board_width]))

    @classmethod
    def add_piece(cls, board, piece_number, placement):
        new_pieces = board.pieces.copy()
        new_pieces.append(piece_number)
        return cls(new_pieces, board._matrix + placement)

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

    # Create all the pieces
    pieces = [Piece(i + 1, piece_shape) for i, piece_shape in enumerate(pieces_shapes)]

    # Precompute all the ways to cover each square on the board
    next_placements = precompute_next_placements(pieces)

    # Uncomment to visually check if pieces have been correctly entered
    # for piece in pieces:
    #     print(piece._matrix)
    # input("Press Enter to continue...")

    # Put an empty board on the stack
    stack = [Board.empty()]

    while stack:

        # Take the first board from the stack
        board = stack.pop()

        # Stop if a solution has been found
        if len(board.pieces) == len(pieces):
            print("Found a solution!")
            print(board._matrix)
            exit()

        # Find the first empty slot
        row, col = board.first_empty_slot()

        # Find all the ways this slot could be covered by a piece, and if the
        # placement is valid make a new board with it and put it on the stack
        for piece_number, piece_placements in next_placements[row][col].items():
            if not board.contains_piece(piece_number):
                for piece_placement in piece_placements:
                    if not board.would_cause_overlap(piece_placement):
                        new_board = Board.add_piece(
                            board, piece_number, piece_placement
                        )
                        stack.append(new_board)


if __name__ == "__main__":
    main()
