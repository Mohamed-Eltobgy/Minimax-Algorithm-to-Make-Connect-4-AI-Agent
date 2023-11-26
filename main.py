import time

import pygame

cols = [3,4,2,1,5,0,6]

def convert_to_tuple(array_2d):
    return tuple(tuple(row) for row in array_2d)


def convert_to_tuple_alpha_beta(array_2d, alpha, beta):
    array_tuple = tuple(tuple(row) for row in array_2d)
    return (array_tuple, alpha, beta)





def count_connected_fours(board, player):
    ROWS = len(board)
    COLUMNS = len(board[0])
    count = 0

    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                count += 1


    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                count += 1

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                count += 1
            if all(board[row + 3 - i][col + i] == player for i in range(4)):
                count += 1

    return count





def Evaluate_V2(board):
    AI, Player, Empty = '2', '1', '0'
    ROWS, COLUMNS = len(board), len(board[0])

    score = 0
    patterns = {
        (4, 0, 0): 1000,  # AI wins
        (3, 0, 1): 700,  # AI is one step from winning
        (2, 0, 2): 30,  # AI has a chance
        (0, 2, 2): -40,  # Player has a chance
        (0, 3, 1): -800,  # Player is one step from winning
        (0, 4, 0): -1500  # Player wins
    }

    # Horizontal, Vertical, Diagonal Down-right, Diagonal Up-right checks
    for row in range(ROWS):
        if board[row][COLUMNS // 2] == AI:
            score += 15
        elif board[row][COLUMNS // 2] == Player:
            score -= 20
        for col in range(COLUMNS):
            if col <= COLUMNS - 4:
                # Horizontal check
                line = board[row][col:col + 4]
                ai_count = line.count(AI)
                player_count = line.count(Player)
                score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

            if row <= ROWS - 4:
                # Vertical check
                line = [board[row + i][col] for i in range(4)]
                ai_count = line.count(AI)
                player_count = line.count(Player)
                score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

                if col <= COLUMNS - 4:
                    # Diagonal Down-right check
                    line = [board[row + i][col + i] for i in range(4)]
                    ai_count = line.count(AI)
                    player_count = line.count(Player)
                    score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

            if row >= 3 and col <= COLUMNS - 4:
                # Diagonal Up-right check
                line = [board[row - i][col + i] for i in range(4)]
                ai_count = line.count(AI)
                player_count = line.count(Player)
                score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

    return score


def Evaluate(board):
    return Evaluate_V2(board)


def isTerminal(state):
    for i in range(7):
        if state[5][i] == '0':
            return False
    return True


def getChildren(state, IsMaximizing):

    if IsMaximizing:
        player = '2'
    else:
        player = '1'
    children = []
    for i in cols:
        if not isValidMove(state,i):
            continue
        tmp = [row[:] for row in state]
        for j in range(len(state)):
            if tmp[j][i] == '0':
                tmp[j][i] = player
                children.append(tmp.copy())
                break
    return children


def isValidMove(board, col):
    if board[len(board) - 1][col] != '0':
        return False

    return True


def makeMove(board, col, player):
    for i in range(len(board)):
        if board[i][col] == '0':
            board[i][col] = player
            break
    return board


def make_agent_move(board, depth, alpha_beta):
    best_score = float('-inf')
    best_move = None
    mpMax = {}
    mpMin = {}


    for col in cols:
        if isValidMove(board, col):
            temp_board = [['0' for _ in range(len(board[0]))] for _ in range(len(board))]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    temp_board[i][j] = board[i][j]

            temp_board = makeMove(temp_board, col, '2')

            if not alpha_beta:
                score = minimax(temp_board, depth - 1, False, mpMax, mpMin)
            else:
                score = minimax_alpha_beta(temp_board, depth - 1, False, mpMax, mpMin, best_score, float('inf'))
                mpMax[tuple] = score

            if score > best_score:
                best_score = score
                best_move = col


    print("score = ", best_score)
    return best_move


def minimax(state, k, IsMaximizing, mpMax, mpMin):
    if k < 0 or isTerminal(state):
        score = Evaluate(state)
        return score

    tupleState = convert_to_tuple(state)

    if (IsMaximizing):
        if tupleState in mpMax:
            return mpMax[tupleState]

        bestValue = float('-inf')
        children = getChildren(state, IsMaximizing)

        for child in children:
            value = minimax(child, k - 1, False, mpMax, mpMin)
            bestValue = max(value, bestValue)

        mpMax[tupleState] = bestValue
        return bestValue

    else:
        if tupleState in mpMin:
            return mpMin[tupleState]
        bestValue = float('inf')
        children = getChildren(state, IsMaximizing)
        for child in children:
            value = minimax(child, k - 1, True, mpMax, mpMin)
            bestValue = min(value, bestValue)

        mpMin[tupleState] = bestValue
        return bestValue


def minimax_alpha_beta(state, k, IsMaximizing, mpMax, mpMin, alpha=float('-inf'), beta=float('inf')):
    if k < 0 or isTerminal(state):
        score = Evaluate(state)
        return score

    tupleState = convert_to_tuple_alpha_beta(state, alpha, beta)

    if IsMaximizing:
        if tupleState in mpMax:

            return mpMax[tupleState]

        bestValue = float('-inf')
        children = getChildren(state, IsMaximizing)

        for child in children:
            value = minimax_alpha_beta(child, k - 1, False, mpMax, mpMin, alpha, beta)
            bestValue = max(value, bestValue)
            alpha = max(alpha, bestValue)

            if beta <= alpha:
                break

        mpMax[tupleState] = bestValue
        return bestValue

    else:
        if tupleState in mpMin:
            return mpMin[tupleState]

        bestValue = float('inf')
        children = getChildren(state, IsMaximizing)
        for child in children:
            value = minimax_alpha_beta(child, k - 1, True, mpMax, mpMin, alpha, beta)
            bestValue = min(value, bestValue)
            beta = min(beta, bestValue)

            if beta <= alpha:
                break

        mpMin[tupleState] = bestValue
        return bestValue


# Draw the Connect-4 board
def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):

            pygame.draw.rect(screen, (0, 0, 250), (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            pygame.draw.circle(screen, (0, 0, 0),
                               (int(c * SQUARE_SIZE + SQUARE_SIZE // 2), int(r * SQUARE_SIZE + SQUARE_SIZE // 2)),
                               RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            piece_y = (ROWS - 1 - r) * SQUARE_SIZE + SQUARE_SIZE // 2

            if board[r][c] == '1':
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE // 2), int(piece_y)), RADIUS)
            elif board[r][c] == '2':
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE // 2), int(piece_y)), RADIUS)

    pygame.display.update()


# Main game loop
def game_loop():
    board = [['0' for _ in range(COLUMNS)] for _ in range(ROWS)]

    while True:
        turn = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    posx = event.pos[0]
                    col = posx // SQUARE_SIZE
                    if isValidMove(board, col):
                        board = makeMove(board, col, '1')
                        turn += 1
                        turn %= 2

        draw_board(board)
        pygame.display.update()
        if turn == 1:
            t1 = time.time()
            col = make_agent_move(board, 10,True)
            board = makeMove(board, col, '2')
            t2 = time.time()
            print("time = ", t2 - t1)
            turn += 1
            turn %= 2
            print("Player count = ", count_connected_fours(board, '1'))
            print("AI count = ", count_connected_fours(board, '2'))
            draw_board(board)
            pygame.display.update()

    pygame.quit()


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 600
ROWS, COLUMNS = 6, 7
SQUARE_SIZE = WIDTH // COLUMNS
RADIUS = SQUARE_SIZE // 2 - 5
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect-4")

game_loop()

# board = [['1','1','1','1','1','1','1'],
#          ['1','1','1','1','1','1','1'],
#          ['1','1','1','1','1','1','1'],
#          ['1','1','1','1','1','1','1'],
#          ['1','1','1','1','1','1','1'],
#          ['1','1','1','1','1','1','1'],
# ]

# print(count_connected_fours(board,'1'))
# x = {}
# x[convert_to_tuple(board)] = 5
# print((1,2) in x)
# print(minimax(board,1,True))
#
# print(count_potential_fours(board,'2'))
# print(isTerminal(board))

# print(minimax(board,6,True))
# print(count_connected_fours(board,'1'))
# print(center_column_control(board,'2'))
# print((getChildren(board)[6]))
