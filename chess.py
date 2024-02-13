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
    
    # Placing the pieces on the board according to the standard starting position
    board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
    board[1] = ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp']
    board[6] = ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp']
    board[7] = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']

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

# Returns a list of all valid moves for a piece
def getAllPossibleMoves(piece, board):
    validMoves = []
    row, col = None, None
    
    # Find the position of the piece on the board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == piece:
                row, col = i, j
                break
        if row is not None:
            break
    
    # Determine valid moves based on the type of the piece
    if piece[1] == 'P':  # Pawn
        validMoves = getPawnMoves((row, col), board)
    elif piece[1] == 'R':  # Rook
        validMoves = getRookMoves((row, col), board)
    elif piece[1] == 'N':  # Knight
        validMoves = getKnightMoves((row, col), board)
    elif piece[1] == 'B':  # Bishop
        validMoves = getBishopMoves((row, col), board)
    elif piece[1] == 'Q':  # Queen
        validMoves = getQueenMoves((row, col), board)
    elif piece[1] == 'K':  # King
        validMoves = getKingMoves((row, col), board)
    
    return validMoves

# Determine all possible squares a pawn can move to
def getPawnMoves(position, board):
    moves = []
    row, col = position
    piece_color = board[row][col][0]
    direction = -1 if piece_color == 'w' else 1
    
    # Forward movement
    if board[row + direction][col] == '--':
        moves.append((row + direction, col))
        # Double square move from starting position
        if ((piece_color == 'w' and row == 6) or (piece_color == 'b' and row == 1)) and \
                board[row + 2 * direction][col] == '--':
            moves.append((row + 2 * direction, col))
    
    # Diagonal captures
    for d in [-1, 1]:
        if 0 <= col + d < DIMENSION:
            if board[row + direction][col + d] != '--' and board[row + direction][col + d][0] != piece_color:
                moves.append((row + direction, col + d))
    
    return moves

# Determine all possible squares a rook can move to
def getRookMoves(position, board):
    moves = []
    row, col = position
    
    # Horizontal moves
    for i in range(row - 1, -1, -1):  # Up
        if board[i][col] == '--':
            moves.append((i, col))
        elif board[i][col][0] != board[row][col][0]:
            moves.append((i, col))
            break
        else:
            break
    for i in range(row + 1, DIMENSION):  # Down
        if board[i][col] == '--':
            moves.append((i, col))
        elif board[i][col][0] != board[row][col][0]:
            moves.append((i, col))
            break
        else:
            break
    
    # Vertical moves
    for i in range(col - 1, -1, -1):  # Left
        if board[row][i] == '--':
            moves.append((row, i))
        elif board[row][i][0] != board[row][col][0]:
            moves.append((row, i))
            break
        else:
            break
    for i in range(col + 1, DIMENSION):  # Right
        if board[row][i] == '--':
            moves.append((row, i))
        elif board[row][i][0] != board[row][col][0]:
            moves.append((row, i))
            break
        else:
            break
    
    return moves

# Determine all possible squares a knight can move to
def getKnightMoves(position, board):
    moves = []
    row, col = position
    for r in range(row - 2, row + 3):
        for c in range(col - 2, col + 3):
            if abs(r - row) + abs(c - col) == 3 and \
                    0 <= r < DIMENSION and 0 <= c < DIMENSION and \
                    board[r][c][0] != board[row][col][0]:
                moves.append((r, c))
    return moves

# Determine all possible squares a bishop can move to
def getBishopMoves(position, board):
    moves = []
    row, col = position
    
    # Diagonal moves
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < DIMENSION and 0 <= c < DIMENSION:
            if board[r][c] == '--':
                moves.append((r, c))
            elif board[r][c][0] != board[row][col][0]:
                moves.append((r, c))
                break
            else:
                break
            r += dr
            c += dc
    
    return moves

# Determine all possible squares a queen can move to
def getQueenMoves(position, board):
    return getRookMoves(position, board) + getBishopMoves(position, board)

# Determine all possible squares a king can move to
def getKingMoves(position, board):
    moves = []
    row, col = position
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and \
                    (r != row or c != col) and board[r][c][0] != board[row][col][0]:
                moves.append((r, c))
    return moves

# Handle the user's clicks
def handleClick(x, y, board, squares):
    if x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
        return None  # Click is outside of the board area
    
    # Convert pixel coordinates to board coordinates
    row = y // SQ_SIZE
    col = x // SQ_SIZE
    
    if board[row][col] != '--':
        return board[row][col]
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

# Create Board object
def createBoardSquares(width, height, sq_size):
    squares = []
    for row in range(DIMENSION):
        row_squares = []
        for col in range(DIMENSION):
            rect = pygame.Rect(col * sq_size, row * sq_size, sq_size, sq_size)
            row_squares.append(rect)
        squares.append(row_squares)
    return squares

# Main game loop
def main():
    squares = createBoardSquares(WIDTH, HEIGHT, SQ_SIZE)
    clock = pygame.time.Clock()
    running = True
    selectedPiecePosition = None
    validMoves = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQ_SIZE, x // SQ_SIZE
                
                # If no piece is selected, try to select one
                if selectedPiecePosition is None:
                    selectedPiecePosition = (row, col)
                    selectedPiece = board[row][col]
                    if selectedPiece != '--':
                        validMoves = getAllPossibleMoves(selectedPiece, board)
                    else:
                        selectedPiecePosition = None
                        validMoves = []
                else:
                    # If a piece is already selected, try to move it
                    if (row, col) in validMoves:
                        # Move the selected piece to the clicked square
                        board[row][col] = board[selectedPiecePosition[0]][selectedPiecePosition[1]]
                        board[selectedPiecePosition[0]][selectedPiecePosition[1]] = '--'
                        selectedPiecePosition = None
                        validMoves = []
                    else:
                        selectedPiecePosition = None
                        validMoves = []
                    
        drawBoard(screen, board, squares, validMoves)
        clock.tick(MAX_FPS)

if __name__ == "__main__":
    main()