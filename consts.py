from classes.Piece import Piece

PLAYER_COLOR_NAMES = [
	"Red",
	"Blue",
	"Green",
	"Yellow"
]

PIECES:list[Piece] = [
    Piece(1, 1, 1, [
        [1]
    ], True, 1), #1
    Piece(2, 1, 1, [
        [1, 1]
    ], True, 2), #2
    Piece(2, 2, 1, [
        [1, 1],
        [1, 0]
    ], True), #L
    Piece(3, 2, 1, [
        [1, 1, 0],
        [0, 1, 1]
    ]), #squiggly
    Piece(2, 2, 1, [
        [1, 1],
        [1, 1]
    ], True, 1), #square
    Piece(3, 2, 1, [
        [1, 1, 1],
        [0, 1, 0]
    ], True), #T
    Piece(3, 2, 1, [
        [1, 1, 1],
        [0, 0, 1]
    ]),
    Piece(3, 1, 1, [
        [1, 1, 1]
    ], True, 2),
    Piece(4, 1, 1, [
        [1, 1, 1, 1]
    ], True, 2),
    Piece(3, 2, 1, [
        [1, 0, 1],
        [1, 1, 1]
    ], True),
    Piece(4, 2, 1, [
        [0, 0, 1, 1],
        [1, 1, 1, 0]
    ]),
    Piece(3, 3, 1, [
        [0, 1, 1],
        [0, 1, 0],
        [1, 1, 0]
    ]),
    Piece(4, 2, 1, [
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ]),
    Piece(3, 3, 1, [
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 0]
    ], True),
    Piece(3, 3, 1, [
        [1, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]),
    Piece(2, 3, 1, [
        [1, 0],
        [1, 1],
        [1, 1]
    ]),
    Piece(3, 3, 1, [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 1]
    ]),
    Piece(5, 1, 1, [
        [1, 1, 1, 1, 1]
    ], True, 2),
    Piece(3, 3, 1, [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ], True, 1),
    Piece(3, 3, 1, [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ], True),
    Piece(4, 2, 1, [
        [1, 1, 1, 1],
        [0, 1, 0, 0]])
]