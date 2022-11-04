"""Backend for generating solutions to a WordHunt board."""
from .dictionary import load_dict


# Load the dictionary
cdef set dictionary = load_dict()


cdef is_word(word: str):
    """
    Checks if a word is a valid dictionary word.
    """
    return word in dictionary


class Board:
    def __init__(self, board: list):
        self.board = board
        self.height = len(board)
        self.width = len(board[0])
        self.x_top = self.width - 1
        self.y_top = self.height - 1
        self.results = []

    @classmethod
    def from_letters(cls, letters: str, width: int, height: int) -> "Board":
        """
        Gathers letters from user input and returns a two-dimensional array.
        """
        cdef int total_characters = width * height
        if not len(letters) == total_characters:
            raise ValueError(
                f"A board with the dimensions you specified has {total_characters} "
                "total letters."
            )

        cdef list board = []
        cdef int counter = 0
        for _ in range(height):
            board.append(letters[counter : counter + width])
            counter += width

        return cls(board)
        

    def query(self, x: int, y: int):
        """
        Return 1, 0 instead of 0, 1 becaues we want to query in the format
        x, y, not y, x.
        """
        return self.board[y][x]

    def solve(self) -> list:
        self.results = all_possibilities(self)
        return self.results

    def print_results(self, limit: int = 1000):
        if not self.results:
            self.solve()

        return print_results(self.results, limit=limit)

    def __str__(self):
        return "\n".join([str(row) for row in self.board])


cdef list _circle_around(tuple coordinates, board: Board):
    """
    Returns all coordinate possibilities of circling around a letter by coordinate.
    """
    def on_grid(coordinates: tuple):
        if 0 <= coordinates[0] <= board.x_top:
            if 0 <= coordinates[1] <= board.y_top:
                return True
        return False

    # Aliases
    c = coordinates
    cdef int x = 0
    cdef int y = 1

    cdef list possibilities = []
    possibilities.append((c[x], c[y] - 1))
    possibilities.append((c[x] + 1, c[y] - 1))
    possibilities.append((c[x] + 1, c[y]))
    possibilities.append((c[x] + 1, c[y] + 1))
    possibilities.append((c[x], c[y] + 1))
    possibilities.append((c[x] - 1, c[y] + 1))
    possibilities.append((c[x] - 1, c[y]))
    possibilities.append((c[x] - 1, c[y] - 1))

    for coordinate in possibilities[:]:
        if not on_grid(coordinate):
            possibilities.remove(coordinate)

    return possibilities


def all_possibilities(board: Board):
    cdef list wordstuple = []

    def duplicate(word) -> bool:
        return word in [_[1] for _ in words]

    cdef int y
    cdef str row
    cdef int x
    cdef str character
    cdef list words = []

    cdef tuple p2
    cdef tuple p3
    cdef tuple p4
    cdef tuple p5
    cdef tuple p6
    cdef tuple p7
    cdef tuple p8
    cdef tuple p9

    for y, row in enumerate(board.board):
        for x, character in enumerate(row):
            for p2 in _circle_around((x, y), board):
                for p3 in _circle_around(p2, board):
                    if p3 in [(x, y), p2]:
                        continue
                    word: str = "".join([character, board.query(*p2), board.query(*p3)])
                    if not duplicate(word) and is_word(word):
                        words.append(((x, y), word))
                    for p4 in _circle_around(p3, board):
                        if p4 in [(x, y), p2, p3]:
                            continue
                        word = "".join(
                            [character, board.query(*p2), board.query(*p3), board.query(*p4)]
                        )
                        if not duplicate(word) and is_word(word):
                            words.append(((x, y), word))
                        for p5 in _circle_around(p4, board):
                            if p5 in [(x, y), p2, p3, p4]:
                                continue
                            word = "".join(
                                [
                                    character,
                                    board.query(*p2),
                                    board.query(*p3),
                                    board.query(*p4),
                                    board.query(*p5),
                                ]
                            )
                            if not duplicate(word) and is_word(word):
                                words.append(((x, y), word))
                            for p6 in _circle_around(p5, board):
                                if p6 in [(x, y), p2, p3, p4, p5]:
                                    continue
                                word = "".join(
                                    [
                                        character,
                                        board.query(*p2),
                                        board.query(*p3),
                                        board.query(*p4),
                                        board.query(*p5),
                                        board.query(*p6),
                                    ]
                                )
                                if not duplicate(word) and is_word(word):
                                    words.append(((x, y), word))
                                for p7 in _circle_around(p6, board):
                                    if p7 in [(x, y), p2, p3, p4, p5, p6]:
                                        continue
                                    word = "".join(
                                        [
                                            character,
                                            board.query(*p2),
                                            board.query(*p3),
                                            board.query(*p4),
                                            board.query(*p5),
                                            board.query(*p6),
                                            board.query(*p7),
                                        ]
                                    )
                                    if not duplicate(word) and is_word(word):
                                        words.append(((x, y), word))
                                    for p8 in _circle_around(p7, board):
                                        if p8 in [(x, y), p2, p3, p4, p5, p6, p7]:
                                            continue
                                        word = "".join(
                                            [
                                                character,
                                                board.query(*p2),
                                                board.query(*p3),
                                                board.query(*p4),
                                                board.query(*p5),
                                                board.query(*p6),
                                                board.query(*p7),
                                                board.query(*p8),
                                            ]
                                        )
                                        if not duplicate(word) and is_word(word):
                                            words.append(((x, y), word))
                                        for p9 in _circle_around(p8, board):
                                            if p9 in [
                                                (x, y),
                                                p2,
                                                p3,
                                                p4,
                                                p5,
                                                p6,
                                                p7,
                                                p8,
                                            ]:
                                                continue
                                            word = "".join(
                                                [
                                                    character,
                                                    board.query(*p2),
                                                    board.query(*p3),
                                                    board.query(*p4),
                                                    board.query(*p5),
                                                    board.query(*p6),
                                                    board.query(*p7),
                                                    board.query(*p8),
                                                    board.query(*p9),
                                                ]
                                            )
                                            if not duplicate(word) and is_word(word):
                                                words.append(((x, y), word))

    # Sort result
    return sorted(words, key=lambda val: len(val[1]), reverse=True)


def print_results(possibilities: list[tuple[int, int], str], limit: int = 1000) -> str:
    res = ""
    for pos, possibility in enumerate(possibilities):
        current = f"{possibility[0][0]+1}, {possibility[0][1]+1} - {possibility[1]}\n"
        res += current
        if pos == limit:
            return res

    return res
