import threading
import time
import pygame
import tkinter as tk
import copy

cols = [3,4,2,1,5,0,6]






class Node:
    def __init__(self, state, value=None):
        self.state = state
        self.value = value
        self.children = []
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
    root = Node(copy.deepcopy(board))
    #print(board)

    for col in cols:
        if isValidMove(board, col):
            temp_board = [['0' for _ in range(len(board[0]))] for _ in range(len(board))]
            for i in range(len(board)):
                for j in range(len(board[0])):
                    temp_board[i][j] = board[i][j]

            temp_board = makeMove(temp_board, col, '2')

            if not alpha_beta:
                score, subtree = minimax(temp_board, depth - 1, False, {}, {})
            else:
                score, subtree = minimax_alpha_beta(temp_board, depth - 1, False, {}, {}, best_score, float('inf'))

            root.children.append(subtree)  # Add the subtree as a child of the root

            if score > best_score:
                best_score = score
                best_move = col

    print("Best score = ", best_score)
    return best_move, root  # Return the best move and the entire decision tree


def minimax(state, k, IsMaximizing, mpMax, mpMin):
    node = Node(state)

    if k <= 0 or isTerminal(state):
        score = Evaluate(state)
        node.value = score
        return score, node

    tupleState = convert_to_tuple(state)

    if IsMaximizing:
        if tupleState in mpMax:
            node.value = mpMax[tupleState]
            print(tupleState)
            return mpMax[tupleState], node

        bestValue = float('-inf')
        children = getChildren(state, IsMaximizing)

        for child in children:
            value, childNode = minimax(child, k - 1, False, mpMax, mpMin)
            node.children.append(childNode)
            bestValue = max(value, bestValue)

        node.value = bestValue
        mpMax[tupleState] = bestValue
        return bestValue, node

    else:
        if tupleState in mpMin:
            node.value = mpMin[tupleState]
            print(tupleState)
            return mpMin[tupleState], node

        bestValue = float('inf')
        children = getChildren(state, IsMaximizing)

        for child in children:
            value, childNode = minimax(child, k - 1, True, mpMax, mpMin)
            node.children.append(childNode)
            bestValue = min(value, bestValue)

        node.value = bestValue
        mpMin[tupleState] = bestValue
        return bestValue, node


def minimax_alpha_beta(state, k, IsMaximizing, mpMax, mpMin, alpha=float('-inf'), beta=float('inf')):
    node = Node(state)

    if k <= 0 or isTerminal(state):
        score = Evaluate(state)
        node.value = score
        return score, node

    tupleState = convert_to_tuple_alpha_beta(state, alpha, beta)

    if IsMaximizing:
        if tupleState in mpMax:
            node.value = mpMax[tupleState]
            return mpMax[tupleState], node

        bestValue = float('-inf')
        children = getChildren(state, IsMaximizing)

        for child in children:
            value, childNode = minimax_alpha_beta(child, k - 1, False, mpMax, mpMin, alpha, beta)
            bestValue = max(value, bestValue)
            alpha = max(alpha, bestValue)
            node.children.append(childNode)

            if beta <= alpha:
                break

        node.value = bestValue
        mpMax[tupleState] = bestValue
        return bestValue, node

    else:
        if tupleState in mpMin:
            node.value = mpMin[tupleState]
            return mpMin[tupleState], node

        bestValue = float('inf')
        children = getChildren(state, IsMaximizing)

        for child in children:
            value, childNode = minimax_alpha_beta(child, k - 1, True, mpMax, mpMin, alpha, beta)
            bestValue = min(value, bestValue)
            beta = min(beta, bestValue)
            node.children.append(childNode)

            if beta <= alpha:
                break

        node.value = bestValue
        mpMin[tupleState] = bestValue
        return bestValue, node

################################ 1st window
import PySimpleGUI as sg

def Get_parameters_window():
    layout = [
        [sg.Text('Depth:'), sg.InputText(key='depth')],
        [sg.Checkbox('Alpha-Beta Pruning', key='alpha_beta'), sg.Checkbox('Show Tree', key='show_tree')],
        [sg.Button('OK')]
    ]

    window = sg.Window('Parameters', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            return None, None, None

        if event == 'OK':
            depth = int(values['depth']) if values['depth'].isdigit() else 0
            alpha_beta = values['alpha_beta']
            show_tree = values['show_tree']
            window.close()
            return depth, alpha_beta, show_tree



##########

##########    TREE
def draw_node(canvas, node, x, y, cell_size=10):  # Reduced cell_size
    columns = len(node.state[0])
    rows = len(node.state)
    grid_width = columns * cell_size
    grid_height = rows * cell_size

    start_x = x - grid_width // 2
    start_y = y - grid_height // 2

    for i in range(rows):
        for j in range(columns):
            cell_x = start_x + j * cell_size
            cell_y = start_y + (rows - 1 - i) * cell_size
            color = "white"
            if node.state[i][j] == '1':
                color = "red"
            elif node.state[i][j] == '2':
                color = "yellow"
            canvas.create_rectangle(cell_x, cell_y, cell_x + cell_size, cell_y + cell_size, fill=color, outline='black')

    score_text = f"Score: {node.value}" if node.value is not None else "Score: N/A"
    canvas.create_text(x, start_y + grid_height + 10, text=score_text, font=('Helvetica', '8'), fill='black')  # Adjusted text position and font size

    return start_x, start_y, start_x + grid_width, start_y + grid_height + 10

import tkinter as tk

# Existing draw_node function remains unchanged

def draw_tree(canvas, node, x, y, node_positions, level_distance=100, sibling_distance=80, cell_size=10, spacing_factor=0.9):
    if not node:
        return

    node_bbox = draw_node(canvas, node, x, y, cell_size)
    node_positions[node] = (node_bbox, node_positions.get(node, (None, False))[1])

    if node_positions[node][1]:
        num_children = len(node.children)
        start_x = x - (num_children - 1) * sibling_distance * spacing_factor / 2

        for idx, child in enumerate(node.children):
            child_x = start_x + idx * sibling_distance * spacing_factor
            child_y = y + level_distance

            canvas.create_line(x, y, child_x, child_y)
            draw_tree(canvas, child, child_x, child_y, node_positions, level_distance, sibling_distance, cell_size, spacing_factor)



def on_canvas_click(event, canvas, root, node_positions):
    for node, (bbox, children_displayed) in node_positions.items():
        if bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
            # Check if the node has children
            if not node.children:  # If the node has no children
                print("Node has no children")  # Print a message to the console
            else:
                # Toggle the display of children
                node_positions[node] = (bbox, not children_displayed)
                redraw_tree(canvas, root, node_positions)
            break


def redraw_tree(canvas, root, node_positions):
    canvas.delete("all")
    initial_x = canvas.winfo_reqwidth()  *2.6
    draw_tree(canvas, root, initial_x, 50, node_positions)

def visualize_tree(root):
    master = tk.Tk()
    master.title("Connect-4 Tree Visualization")


    canvas = tk.Canvas(master)
    canvas.pack(expand=tk.YES, fill=tk.BOTH)  # Make the canvas expand to fill the window3


    node_positions = {}

    initial_x = canvas.winfo_reqwidth() *2.6
    draw_tree(canvas, root, initial_x, 50, node_positions)

    canvas.bind("<Button-1>", lambda event: on_canvas_click(event, canvas, root, node_positions))

    master.mainloop()






###########

# Draw the Connect-4 board
def game_loop():
    board = [['0' for _ in range(COLUMNS)] for _ in range(ROWS)]

    depth, alpha_beta, show_tree = Get_parameters_window()


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
            col,root = make_agent_move(board, depth,alpha_beta)
            board = makeMove(board, col, '2')
            t2 = time.time()

            print("time = ", t2 - t1)
            draw_board(board)
            turn += 1
            turn %= 2
            print("Player count = ", count_connected_fours(board, '1'))
            print("AI count = ", count_connected_fours(board, '2'))
            pygame.display.update()
            if show_tree:
                visualization_thread = threading.Thread(target=visualize_tree, args=(root,))
                visualization_thread.start()

    pygame.quit()

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
