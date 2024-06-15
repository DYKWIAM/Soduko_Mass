import numpy as np

# Constants for text formatting
BOLD = '\033[1m'
RESET = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESETT = '\033[0m'


def is_valid_move(board, row, col, num):
    # Check if the number is already in the row, column, or 3x3 subgrid
    def in_row_col_or_subgrid():
        subgrid_row = 3 * (row // 3)
        subgrid_col = 3 * (col // 3)
        return (
                num in board[row, :] or  # Check whole row
                num in board[:, col] or  # Check whole column
                num in board[subgrid_row:subgrid_row + 3, subgrid_col:subgrid_col + 3]  # Check subgrid
        )

    return not in_row_col_or_subgrid()


def solve_sudoku(board):
    # Find the first empty cell (with value 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  # Found an empty cell
                for num in range(1, 10):
                    if is_valid_move(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0  # Reset cell if solution fails
                return False
    return True


def generate_sudoku(difficulty=75):
    board = np.zeros((9, 9), dtype=int)  # Generate a 9x9 Sudoku board filled with zeros
    solve_sudoku(board)

    # Remove numbers to create the puzzle
    num_to_remove = 81 - difficulty
    cells = np.random.choice(81, num_to_remove, replace=False)
    for cell in cells:
        row, col = divmod(cell, 9)
        board[row, col] = 0

    return board


def print_sudoku(board):
    # Print column labels (0-8)
    print(BOLD + YELLOW + "    0 1 2  3 4 5  6 7 8" + RESET)
    print(" +" + "-" * 21 + "+")

    # Iterate over rows and columns to print the Sudoku board
    for i in range(9):
        print(i, end=' | ')
        for j in range(9):
            print(board[i][j], end=' ')
            if (j + 1) % 3 == 0 and j != 8:
                print("|", end=' ')
        print()
        if (i + 1) % 3 == 0 and i != 8:
            print(" |" + "-" * 21 + "|")

    print(" +" + "-" * 22 + "+")


# Generate a Sudoku board
sudoku_board = generate_sudoku(difficulty=40)
sudoku_board_solved = np.copy(sudoku_board)
print(GREEN + BOLD + "Solved Board." + RESET + RESETT)
solve_sudoku(sudoku_board_solved)
print_sudoku(sudoku_board_solved)
print(GREEN + BOLD + "Unsolved Board." + RESET + RESETT)
print_sudoku(sudoku_board)

# Main game loop to play Sudoku
while True:
    print_sudoku(sudoku_board)
    print(GREEN + BOLD + "To solve the Sudoku, enter the row number, column number, and your answer." + RESET)
    print(RED + "Type 'X' to Exit" + RESET)
    row = input("Enter Row number: ")
    col = input("Enter Column number: ")
    answer = input("Enter your Answer: ")

    # Check if the user wants to exit
    if row.lower() == "x" or col.lower() == "x" or answer.lower() == "x":
        break

    row = int(row)
    col = int(col)
    answer = int(answer)

    # Check if the move is valid and update the Sudoku board
    if is_valid_move(sudoku_board, row, col, answer):
        sudoku_board[row][col] = answer
        print(BLUE + BOLD + "Move successful!" + RESET)
    else:
        print(BLUE + BOLD + "Invalid input. Please type the right answer." + RESET)