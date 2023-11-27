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


def draw_button(screen, text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    smallText = pygame.font.SysFont("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def open_new_window(connect4_snapshot, current_board):
    new_window = pygame.display.set_mode((WIDTH, HEIGHT))  # Size of the new window
    new_window.fill((255, 255, 255))  # White background for the new window

    # The parent node position (centered at the top of the window)
    parent_pos = (WIDTH // 2 - 50, 50)  # Adjust Y offset as needed for your layout

    # Calculate children positions below the parent
    children_positions = [(i * (WIDTH // 7) + (WIDTH // 14) - 50, 200) for i in range(7)]  # Adjust Y offset as needed

    # Draw the parent node
    parent_surface = visualize_board(current_board, 100, 100)
    new_window.blit(parent_surface, parent_pos)

    # Store rects and corresponding boards for clickable areas
    clickable_areas = []

    # Draw the first layer of children and store their rects
    child_boards = getChildren(current_board, True)
    for i, child_board in enumerate(child_boards):
        child_surface = visualize_board(child_board, 100, 100)
        pos = children_positions[i]
        new_window.blit(child_surface, pos)
        clickable_areas.append((pygame.Rect(pos[0], pos[1], 100, 100), child_board))

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, child_board in clickable_areas:
                    if rect.collidepoint(mouse_pos):
                        # When a child node is clicked, show its children
                        show_children_of_node(new_window, child_board, rect)

        pygame.display.update()


def show_children_of_node(window, board, parent_rect):
    # Clear the window
    window.fill((255, 255, 255))

    # Redraw the parent node at the top
    parent_surface = visualize_board(board, parent_rect.width, parent_rect.height)
    # Use the same X coordinate but place it at the top
    parent_new_pos = (parent_rect.x, 50)  # Y offset to place the parent at the top
    window.blit(parent_surface, parent_new_pos)

    # Calculate new positions for children based on the new parent position
    children_positions = [(i * (WIDTH // 7) + (WIDTH // 14) - 50, parent_new_pos[1] + 150) for i in range(7)]

    # Draw the children of the new parent
    child_boards = getChildren(board, True)
    for i, child_board in enumerate(child_boards):
        child_surface = visualize_board(child_board, 100, 100)
        pos = children_positions[i]
        window.blit(child_surface, pos)

    # Update the display
    pygame.display.update()


def visualize_board(board, width, height):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    square_size = min(width // cols, height // rows)

    # If the radius is too small, pieces will not be visible, so ensure a minimum size
    min_radius = 5
    radius = max(square_size // 2 - 5, min_radius)

    # Create a new surface for the child board with a white background
    surface = pygame.Surface((width, height))
    surface.fill((255, 255, 255))

    # Adjust the drawing for smaller sizes
    for c in range(cols):
        for r in range(rows):
            # Calculate the position and size of each grid cell and piece
            cell_x = c * square_size
            # Start drawing from the bottom of the surface.
            # We subtract from 'rows' instead of 'height' to flip the y-axis.
            cell_y = (rows - 1 - r) * square_size
            piece_x = cell_x + square_size // 2
            piece_y = cell_y + square_size // 2

            # Draw the grid cell
            pygame.draw.rect(surface, (0, 0, 255), (cell_x, cell_y, square_size, square_size))

            # Draw the piece if there is one
            if board[r][c] == '1':
                pygame.draw.circle(surface, RED, (piece_x, piece_y), radius)
            elif board[r][c] == '2':
                pygame.draw.circle(surface, YELLOW, (piece_x, piece_y), radius)

    return surface



# Main game loop
def game_loop():
    board = [['0' for _ in range(COLUMNS)] for _ in range(ROWS)]
    button_x, button_y = (WIDTH - button_width) / 2, HEIGHT - button_height - 10

    while True:
        turn = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x + button_width > event.pos[0] > button_x and button_y + button_height > event.pos[1] > button_y:
                    # Capture Connect 4 window snapshot before opening the new window
                    connect4_snapshot = pygame.display.get_surface().copy()
                    open_new_window(connect4_snapshot, board)
                elif turn == 0:
                    posx = event.pos[0]
                    col = posx // SQUARE_SIZE
                    if isValidMove(board, col):
                        board = makeMove(board, col, '1')
                        turn += 1
                        turn %= 2

        draw_board(board)
        draw_button(screen, "New Window", button_x, button_y, button_width, button_height, (100, 200, 100), (100, 255, 100))
        pygame.display.update()

        if turn == 1:
            t1 = time.time()
            col = make_agent_move(board, 3, False)
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
WIDTH, HEIGHT = 900, 800
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
button_width, button_height = 100, 50

game_loop()

