import time

import pygame

def convert_to_tuple(array_2d):
    return tuple(tuple(row) for row in array_2d)




def count_potential_fours(board, player):
    ROWS = len(board)
    COLUMNS = len(board[0])
    potential_fours = 0

    # Check horizontal potential fours
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r][c+i] for i in range(4)]
            if window.count(player) == 3 and window.count('0') == 1:
                potential_fours += 1

    # Check vertical potential fours
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            window = [board[r+i][c] for i in range(4)]
            if window.count(player) == 3 and window.count('0') == 1:
                potential_fours += 1

    # Check positively sloped diagonal potential fours
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            if window.count(player) == 3 and window.count('0') == 1:
                potential_fours += 1

    # Check negatively sloped diagonal potential fours
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            if window.count(player) == 3 and window.count('0') == 1:
                potential_fours += 1

    return potential_fours



def count_connected_fours(board,player):
    ROWS = len(board)
    COLUMNS = len(board[0])
    count = 0
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                count += 1

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                count += 1

    # Diagonal checks
    # Down-right and Up-right
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                count += 1
            if all(board[row + 3 - i][col + i] == player for i in range(4)):
                count += 1

    return count

def center_column_control(board, player):
    ROWS = len(board)
    CENTER_COLUMN = len(board[0]) // 2
    return sum(1 for row in range(ROWS) if board[row][CENTER_COLUMN] == player)




def Evaluate_V2(board):
    AI, Player, Empty = '2', '1', '0'
    ROWS, COLUMNS = len(board), len(board[0])

    score = 0
    # Patterns to look for and their scores
    patterns = {
        (4, 0, 0): 1000,  # AI wins
        (3, 0, 1): 700,   # AI is one step from winning
        (2, 0, 2): 10,    # AI has a chance
        (0, 3, 1): -710,  # Player is one step from winning
        (0, 4, 0): -1000  # Player wins
    }

    # Horizontal, Vertical, Diagonal Down-right, Diagonal Up-right checks
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4:
                # Horizontal check
                line = board[row][col:col+4]
                ai_count = line.count(AI)
                player_count = line.count(Player)
                score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

            if row <= ROWS - 4:
                # Vertical check
                line = [board[row+i][col] for i in range(4)]
                ai_count = line.count(AI)
                player_count = line.count(Player)
                score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

                if col <= COLUMNS - 4:
                    # Diagonal Down-right check
                    line = [board[row+i][col+i] for i in range(4)]
                    ai_count = line.count(AI)
                    player_count = line.count(Player)
                    score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

            if row >= 3 and col <= COLUMNS - 4:
                # Diagonal Up-right check
                line = [board[row-i][col+i] for i in range(4)]
                ai_count = line.count(AI)
                player_count = line.count(Player)
                score += patterns.get((ai_count, player_count, 4 - ai_count - player_count), 0)

    return score


def Evaluate(board):
    score = Evaluate_V2(board)
    #score = 0
    #score += count_connected_fours(board, '2') * 1000
    score += center_column_control(board, '2') * 200
    #score -= count_connected_fours(board, '1') * 1000
    # score += count_potential_fours(board,'2')*500
    # score -= count_potential_fours(board, '1') * 700

    return score


def isTerminal(state):
    if state[5].count('0') == 0 :
        return True
    return False

def getChildren(state,IsMaximizing):
    if(IsMaximizing):
        player = '2'
    else:
        player = '1'
    children = []
    for i in range(len(state[0])):
        tmp = [row[:] for row in state]
        for j in range(len(state)):
            if tmp[j][i] == '0':
                tmp[j][i] = player
                children.append(tmp.copy())
                break
    return children

def isValidMove(board,col):
    if(board[len(board)-1][col] != '0'):
        return False

    return True

def makeMove(board,col,player):
    for i in range(len(board)):
        if(board[i][col] == '0'):
            board[i][col] = player
            break
    return board

def make_agent_move(board,depth):
    best_score = float('-inf')
    best_move = None
    mpMax = {}
    mpMin = {}
    for col in range(len(board[0])):
        if isValidMove(board,col):
            temp_board = [['0' for _ in range(len(board[0]))] for _ in range(len(board))]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    temp_board[i][j] = board[i][j]

            temp_board = makeMove(temp_board,col,'2')
            tuple = convert_to_tuple(temp_board)
            if(tuple in mpMax):
                score = mpMax[tuple]
            elif tuple in mpMin:
                score = mpMin[tuple]
            else:
                score = minimax(temp_board,depth-1,False, mpMax,mpMin)

            if(score > best_score):
                best_score = score
                best_move = col

    return best_move


def minimax(state, k, IsMaximizing, mpMax,mpMin):
    #print("Entered Minimax")
    if( k < 0 or isTerminal(state)):
        score = Evaluate(state)
        return score


    tupleState = convert_to_tuple(state)


    if(IsMaximizing):
        if tupleState in mpMax:
            #print("Found in max")
            return mpMax[tupleState]

        bestValue = float('-inf')
        children = getChildren(state,IsMaximizing)
        for child in children:
            value = minimax(child,k-1,False,mpMax,mpMin)
            bestValue = max(value, bestValue)

        mpMax[tupleState] = bestValue
        return bestValue

    else:
        if tupleState in mpMin:
            #print("found in Min")
            return mpMin[tupleState]
        bestValue = float('inf')
        children = getChildren(state,IsMaximizing)
        for child in children:
            value = minimax(child,k-1,True,mpMax,mpMin)
            bestValue = min(value, bestValue)

        mpMin[tupleState] = bestValue
        return bestValue




# Draw the Connect-4 board
def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            # Draw the blue rectangles for the board
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Draw the white circles for empty slots
            pygame.draw.circle(screen, WHITE, (int(c * SQUARE_SIZE + SQUARE_SIZE // 2), int(r * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)

    # Draw the pieces based on the current board state, from bottom to top
    for c in range(COLUMNS):
        for r in range(ROWS):  # No need to reverse the order of rows
            # Calculate the y position for the piece based on the row number
            # Pieces need to be drawn from the bottom up, so we subtract the row number from ROWS - 1
            piece_y = (ROWS - 1 - r) * SQUARE_SIZE + SQUARE_SIZE // 2

            if board[r][c] == '1':
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE // 2), int(piece_y)), RADIUS)
            elif board[r][c] == '2':
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE // 2), int(piece_y)), RADIUS)

    pygame.display.update()





# Main game loop
def game_loop():
    board = [['0' for _ in range(COLUMNS)] for _ in range(ROWS)]
    #print(board)
    AI_Counter = 0


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
                        turn+=1
                        turn%=2


        draw_board(board)
        pygame.display.update()
        if turn == 1 :
            t1 = time.time()
            col = make_agent_move(board,5)
            board = makeMove(board,col,'2')
            t2 = time.time()
            print("time = ",t2-t1)
            AI_Counter+=1
            turn+=1
            turn%=2
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

# board = [['2','0','0','0','0','0','0'],
#          ['1','0','0','0','0','0','0'],
#          ['2','0','0','0','0','0','0'],
#          ['2','0','0','0','0','0','0'],
#          ['2','0','0','0','0','0','0'],
#          ['0','0','0','0','0','0','0'],
# ]
# x = {}
# x[convert_to_tuple(board)] = 5
# print((1,2) in x)
# print(minimax(board,1,True))
#
# print(count_potential_fours(board,'2'))
#print(isTerminal(board))

#print(minimax(board,6,True))
#print(count_connected_fours(board,'1'))
#print(center_column_control(board,'2'))
#print((getChildren(board)[6]))
