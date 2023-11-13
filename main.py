import pygame





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
    AI = '2'
    Player = '1'
    ROWS = len(board)
    COLUMNS = len(board[0])

    score = 0
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            count1 = 0
            count2 = 0
            count3 = 0
            for i in range (4):
                if board[row][col + i] == AI :
                    count2+=1
                elif board[row][col + i] == Player:
                    count1+=1
                elif board[row][col + i] == '0':
                    count3 += 1

            if(count2 == 4):
                score+=1000
            elif count2 == 3 and count3 == 1 :
                score+=300
            elif count2 == 2 and count3 == 2:
                score +=10
            elif count1 == 3 and count3 == 1:
                score -=700

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            count1 = 0
            count2 = 0
            count3 = 0
            for i in range(4):
                if board[row+i][col] == AI:
                    count2 += 1
                elif board[row+i][col] == Player:
                    count1 += 1
                elif board[row+i][col] == '0':
                    count3 += 1

            if(count2 == 4):
                score+=1000
            elif count2 == 3 and count3 == 1 :
                score+=300
            elif count2 == 2 and count3 == 2:
                score +=10
            elif count1 == 3 and count3 == 1:
                score -=700

    # Diagonal checks
    # Down-right and Up-right
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            count1 = 0
            count2 = 0
            count3 = 0
            for i in range(4):
                if board[row+i][col + i] == AI:
                    count2 += 1
                elif board[row+i][col + i] == Player:
                    count1 += 1
                elif board[row+i][col + i] == '0':
                    count3 += 1

            if(count2 == 4):
                score+=1000
            elif count2 == 3 and count3 == 1 :
                score+=300
            elif count2 == 2 and count3 == 2:
                score +=10
            elif count1 == 3 and count3 == 1:
                score -=700

            count1 = 0
            count2 = 0
            count3 = 0
            for i in range(4):
                if board[row+3-i][col + i] == AI:
                    count2 += 1
                elif board[row+3-i][col + i] == Player:
                    count1 += 1
                elif board[row+3-i][col + i] == '0':
                    count3 += 1

            if(count2 == 4):
                score+=1000
            elif count2 == 3 and count3 == 1 :
                score+=300
            elif count2 == 2 and count3 == 2:
                score +=10
            elif count1 == 3 and count3 == 1:
                score -=700
    return score
def Evaluate(board):
    #score = Evaluate_V2(board)
    score = 0
    score += count_connected_fours(board, '2') * 1000
    score += center_column_control(board, '2') * 50
    score += count_potential_fours(board,'2')*500
    score -= count_potential_fours(board, '1') * 300

    return score


def isTerminal(state):
    if state[0].count('0') == 0 :
        return False
    return True

def getChildren(state):
    children = []
    for i in range(len(state[0])):
        tmp = [row[:] for row in state]
        for j in range(len(state)):
            if tmp[j][i] == '0':
                tmp[j][i] = '2'
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
    for col in range(len(board[0])):
        if isValidMove(board,col):
            temp_board = [['0' for _ in range(len(board[0]))] for _ in range(len(board))]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    temp_board[i][j] = board[i][j]

            temp_board = makeMove(temp_board,col,'2')
            score = minimax(temp_board,depth,False)

            if(score > best_score):
                best_score = score
                best_move = col

    return best_move


def minimax(state, k, IsMaximizing):
    print("Entered Minimax")
    if( k <= 0 or isTerminal(state)):
        return Evaluate(state)
    print("H = ", k)

    if(IsMaximizing):
        bestValue = float('-inf')
        children = getChildren(state)
        for child in children:
            value = minimax(child,k-1,False)
            bestValue = max(value, bestValue)
        return bestValue

    else:
        bestValue = float('inf')
        children = getChildren(state)
        for child in children:
            value = minimax(child,k-1,True)
            bestValue = min(value, bestValue)
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
    print(board)


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
            col = make_agent_move(board,1)
            board = makeMove(board,col,'2')
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
#
# print(count_potential_fours(board,'2'))
#print(isTerminal(board))

#print(minimax(board,6,True))
#print(count_connected_fours(board,'1'))
#print(center_column_control(board,'2'))
#print((getChildren(board)[6]))
