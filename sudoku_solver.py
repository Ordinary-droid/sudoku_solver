def print_board(board):
    """Prints the Sudoku board in a readable format."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


def is_valid(board, row, col, num):
    """Checks if placing num at board[row][col] is valid according to Sudoku rules."""
    # Check the row
    for x in range(9):
        if board[row][x] == num:
            return False

    # Check the column
    for x in range(9):
        if board[x][col] == num:
            return False

    # Check the 3x3 grid
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True


def find_empty_location(board):
    """Finds an empty cell in the Sudoku board. Returns (row, col) or None if full."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  # 0 indicates an empty cell
                return (i, j)
    return None


def solve_sudoku(board):
    """Solves the Sudoku board using backtracking."""
    empty_cell = find_empty_location(board)

    # If no empty cell is found, the puzzle is solved
    if not empty_cell:
        return True

    row, col = empty_cell

    # Try numbers from 1 to 9
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num  # Place the number

            # Recursively attempt to solve the rest of the board
            if solve_sudoku(board):
                return True

            # If placing num didn't lead to a solution, reset and backtrack
            board[row][col] = 0

    return False  # Trigger backtracking


# Example Sudoku puzzle (0 represents empty cells)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if solve_sudoku(sudoku_board):
    print("Sudoku solved successfully!")
else:
    print("No solution exists.")

print_board(sudoku_board)