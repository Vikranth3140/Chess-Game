import pygame

# Set up some constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation
IMAGES = {}

# Initialize a dictionary of images
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('images/' + piece + '.png')

# Initialize the board
def initializeBoard():
    board = [['--' for _ in range(DIMENSION)] for _ in range(DIMENSION)]
    
    board[0][0], board[7][0] = 'bR', 'wR'
    board[0][1], board[7][1] = 'bN', 'wN'
    board[0][2], board[7][2] = 'bB', 'wB'
    board[0][3], board[7][3] = 'bQ', 'wQ'
    board[0][4], board[7][4] = 'bK', 'wK'
    board[0][5], board[7][5] = 'bB', 'wB'
    board[0][6], board[7][6] = 'bN', 'wN'
    board[0][7], board[7][7] = 'bR', 'wR'

    # Now for the pawns
    for col in range(8):
        board[1][col] = 'bP'
        board[6][col] = 'wP'

    return board


# Initialize Pygame
pygame.init()

# Load the images
loadImages()

# Initialize the board
board = initializeBoard()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Determine all possible squares a pawn can move to
def getPawnMoves(position, board):
    moves = []
    row, col = position
    if board[row][col][0] == 'w':
        if row-1 >= 0:
            if board[row-1][col] == '--':
                moves.append((row-1, col))
            if col-1 >= 0 and board[row-1][col-1][0] == 'b':
                moves.append((row-1, col-1))
            if col+1 < DIMENSION and board[row-1][col+1][0] == 'b':
                moves.append((row-1, col+1))
            if row == 6 and board[row-2][col] == '--':
                moves.append((row-2, col))
    else:
        if row+1 < DIMENSION:
            if board[row+1][col] == '--':
                moves.append((row+1, col))
            if col-1 >= 0 and board[row+1][col-1][0] == 'w':
                moves.append((row+1, col-1))
            if col+1 < DIMENSION and board[row+1][col+1][0] == 'w':
                moves.append((row+1, col+1))
            if row == 1 and board[row+2][col] == '--':
                moves.append((row+2, col))
    return moves


# Determine all possible squares a rook can move to
def getRookMoves(position, board):
    moves = []
    row, col = position
    # up
    for i in range(row-1, -1, -1):
        if board[i][col] == '--':
            moves.append((i, col))
        elif board[i][col][0] != board[row][col][0]:
            moves.append((i, col))
            break
    # down
    for i in range(row+1, DIMENSION):
        if board[i][col] == '--':
            moves.append((i, col))
        elif board[i][col][0] != board[row][col][0]:
            moves.append((i, col))
            break
    # left
    for i in range(col-1, -1, -1):
        if board[row][i] == '--':
            moves.append((row, i))
        elif board[row][i][0] != board[row][col][0]:
            moves.append((row, i))
            break
    # right
    for i in range(col+1, DIMENSION):
        if board[row][i] == '--':
            moves.append((row, i))
        elif board[row][i][0] != board[row][col][0]:
            moves.append((row, i))
            break
    return moves


# Determine all possible squares a knight can move to
def getKnightMoves(position, board):
    moves = []
    row, col = position
    for r in range(row-2, row+3):
        for c in range(col-2, col+3):
            if (r-row)**2 + (c-col)**2 == 5 and \
                r >= 0 and r < DIMENSION and \
                c >= 0 and c < DIMENSION:
                if board[r][c] == '--':
                    moves.append((r, c))
                elif board[r][c][0] != board[row][col][0]:
                    moves.append((r, c))
    return moves


# Determine all possible squares a bishop can move to
def getBishopMoves(position, board):
    moves = []
    row, col = position
    for i in range(1, DIMENSION):
        # up-right
        if row-i >= 0 and col+i < DIMENSION:
            if board[row-i][col+i] == '--':
                moves.append((row-i, col+i))
            elif board[row-i][col+i][0] != board[row][col][0]:
                moves.append((row-i, col+i))
                break
        # up-left
        if row-i >= 0 and col-i >= 0:
            if board[row-i][col-i] == '--':
                moves.append((row-i, col-i))
            elif board[row-i][col-i][0] != board[row][col][0]:
                moves.append((row-i, col-i))
                break
        # down-right
        if row+i < DIMENSION and col+i < DIMENSION:
            if board[row+i][col+i] == '--':
                moves.append((row+i, col+i))
            elif board[row+i][col+i][0] != board[row][col][0]:
                moves.append((row+i, col+i))
                break
        # down-left
        if row+i < DIMENSION and col-i >= 0:
            if board[row+i][col-i] == '--':
                moves.append((row+i, col-i))
            elif board[row+i][col-i][0] != board[row][col][0]:
                moves.append((row+i, col-i))
                break
    return moves


# Determine all possible squares a queen can move to
def getQueenMoves(position, board):
    moves = []
    row, col = position
    moves.extend(getRookMoves(position, board))
    moves.extend(getBishopMoves(position, board))
    return moves


# Determine all possible squares a king can move to
def getKingMoves(position, board):
    moves = []
    row, col = position
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if (r-row)**2 + (c-col)**2 <= 2 and \
                r >= 0 and r < DIMENSION and \
                c >= 0 and c < DIMENSION:
                if board[r][c] == '--':
                    moves.append((r, c))
                elif board[r][c][0] != board[row][col][0]:
                    moves.append((r, c))
    return moves


# Handle the user's clicks
def handleClick(x, y, board, squares):
    if (x//SQ_SIZE + y//SQ_SIZE) % 2 == 0:
        square = (x//SQ_SIZE, y//SQ_SIZE)
    else:
        square = (x//SQ_SIZE + 1, y//SQ_SIZE)
    if board[square[0]][square[1]] != '--':
        return board[square[0]][square[1]]
    else:
        return None


# Highlight the possible moves for a piece
def highlightSquares(screen, moves, squares):
    for move in moves:
        row, col = move
        pygame.draw.rect(screen, (0, 255, 0), squares[row][col])


# Draw the board and pieces
def drawBoard(screen, board, squares, highlight):
    screen.fill((0, 0, 0))
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            square = squares[row][col]
            pygame.draw.rect(screen, (255, 255, 255), square)
            if board[row][col] != '--':
                screen.blit(IMAGES[board[row][col]], square)
    if highlight:
        highlightSquares(screen, highlight, squares)
    pygame.display.flip()


# Main game loop
def main():
    loadImages()
    squares = createBoardSquares(WIDTH, HEIGHT, SQ_SIZE)
    clock = pygame.time.Clock()
    running = True
    selectedPiece = None
    validMoves = []
    board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selectedPiece is None:
                    x, y = pygame.mouse.get_pos()
                    selectedPiece = handleClick(x, y, board, squares)
                    if selectedPiece is not None:
                        validMoves = getAllPossibleMoves(selectedPiece, board)
                else:
                    x, y = pygame.mouse.get_pos()
                    row, col = x // SQ_SIZE, y // SQ_SIZE
                    if (row, col) in validMoves:
                        board[row][col] = selectedPiece
                        board[selectedPiece.position[0]][selectedPiece.position[1]] = '--'
                        selectedPiece.position = (row, col)
                    selectedPiece = None
                    validMoves = []
        drawBoard(screen, board, squares, validMoves)
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()