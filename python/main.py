import time
import os
import matplotlib.pyplot as plt
import numpy as np

visualizeAI = False

# Initialize a 3x3 grid for Tic-Tac-Toe
grid = [[' ' for _ in range(3)] for _ in range(3)]

def welcome_message():
    message = "----Welcome to Tic-Tac-Toe----"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    for _ in range(2):
        print('\r' + ' ' * len(message), end='', flush=True)
        time.sleep(0.25)
        print('\r' + message, end='', flush=True)
        time.sleep(0.25)
    print()

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = float('-inf')
    move = None
    scores = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if grid[i][j] == ' ':
                grid[i][j] = 'O'
                score = minimax(grid, 0, False)
                grid[i][j] = ' '
                scores[i][j] = score
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        grid[move[0]][move[1]] = 'O'
    if visualizeAI:
        plot_heatmap(scores)

def plot_heatmap(scores):
    fig, ax = plt.subplots()
    cax = ax.matshow(scores, cmap='coolwarm')
    fig.colorbar(cax)

    for i in range(3):
        for j in range(3):
            if grid[i][j] != ' ':
                ax.text(j, i, grid[i][j], va='center', ha='center', color='black', fontsize=12)
            else:
                ax.text(j, i, f'{scores[i][j]:.2f}', va='center', ha='center', color='white', fontsize=8)

    plt.title('AI Move Scores and Current Grid')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.show()

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def print_grid():
    for row in grid:
        print(' | '.join(row))
        print('-' * 9)


def main():
    global visualizeAI
    while True:
        game_mode = input("Do you want to play against another player or the AI? (Enter 'player' or 'AI'): ").strip().lower()
        if game_mode == 'ai':
            visualizeAI = input("Do you want to visualize the AI's moves with a heatmap? (Enter 'yes' or 'no'): ").strip().lower() == 'yes'
        if game_mode in ['player', 'ai']:
            break
        else:
            print("Invalid input. Please enter 'player' or 'AI'.")

    print("Initial grid:")
    print_grid()

    current_player = 'X'

    while not check_winner(grid) and not is_board_full(grid):
        if current_player == 'O':
            if game_mode == 'ai':
                print("\nMaking the best move for 'O':")
                best_move()
            else:
                while True:
                    try:
                        print("\nPlayer 'O', it's your turn. Enter your move (row and column):")
                        row, col = map(int, input("Enter row and column numbers (1, 2, or 3) separated by space: ").split())
                        row -= 1
                        col -= 1
                        if grid[row][col] == ' ':
                            grid[row][col] = 'O'
                            break
                        else:
                            print("Invalid move. The cell is already occupied. Try again.")
                    except (ValueError, IndexError):
                        print("Invalid input. Please enter row and column numbers (1, 2, or 3) separated by space.")
        else:
            while True:
                try:
                    print("\nYour turn 'X'. Enter your move (row and column):")
                    row, col = map(int, input("Enter row and column numbers (1, 2, or 3) separated by space: ").split())
                    row -= 1
                    col -= 1
                    if grid[row][col] == ' ':
                        grid[row][col] = 'X'
                        break
                    else:
                        print("Invalid move. The cell is already occupied. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter row and column numbers (1, 2, or 3) separated by space.")

        os.system('cls' if os.name == 'nt' else 'clear')
        print_grid()
        current_player = 'O' if current_player == 'X' else 'X'

    winner = check_winner(grid)
    if winner:
        print(f"\nThe winner is {winner}!")
    else:
        print("\nThe game is a tie!")

if __name__ == "__main__":
    main()
