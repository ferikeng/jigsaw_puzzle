import numpy as np
import ipdb

# Define pieces
# Define board

# optimisation: pre-calculate all piece/rotation/positions that cover each slot


# put an empty board on the stack
# repeat:
#   take the first board from the stack
#   find the first empty slot
#   for every piece/rotation/position that covers that slot
#       if there are no overlaps (optimisation: and a feasible solution cannot be ruled out)
#           place the piece
#           put board on the stack


board_width = 5
pieces_shapes = [[(0, 0), (0, 1), (0, 2), (1, 0)], [(0, 0), (0, 1)]]


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

    def __init__(self, pos_tuples) -> None:
        matrix = np.zeros([board_width, board_width])
        for tuple in pos_tuples:
            matrix[tuple[0], tuple[1]] = 1
        self._matrix = matrix
        self._all_placements = Piece._gen_all_placements(self._matrix)


def main():
    board = np.zeros([board_width, board_width])

    pieces = [Piece(piece_shape) for piece_shape in pieces_shapes]

    ipdb.set_trace()


if __name__ == "__main__":
    main()
