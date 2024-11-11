import tkinter as tk
from tkinter import messagebox
import random


class SudokuSolver:
    def __init__(self, master, generate_random=False):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.config(bg="#f2f2f2")  # Light grey background

        # Initialize 9x9 grids for the puzzle and entries
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.generate_random = generate_random  # Flag for generating random puzzle

        self.create_widgets()

        # Generate a random Sudoku puzzle if specified
        if generate_random:
            self.generate_random_sudoku()

    def create_widgets(self):
        # Create a frame for the Sudoku grid
        grid_frame = tk.Frame(self.master, bg="#f2f2f2", padx=10, pady=10)
        grid_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create 9x9 grid of entry boxes for user input
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(grid_frame, font=('Arial', 18),
                                 justify='center', width=2, borderwidth=1, relief="solid", fg="black")
                entry.grid(row=i, column=j, sticky="nsew", padx=(1, 1 if (j + 1) % 3 != 0 else 5),
                           pady=(1, 1 if (i + 1) % 3 != 0 else 5))
                self.entries[i][j] = entry
                entry.config(bg="white" if (i // 3 + j // 3) % 2 ==
                             0 else "#e6e6e6")  # Checkerboard effect for grid

        # Configure grid layout to be responsive
        for i in range(9):
            grid_frame.grid_rowconfigure(i, weight=1)
            grid_frame.grid_columnconfigure(i, weight=1)

        # Create a frame for the control buttons
        button_frame = tk.Frame(self.master, bg="#f2f2f2")
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        # Solve button
        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_sudoku, font=('Arial', 14, 'bold'),
                                 bg="#4CAF50", fg="white", relief="raised", borderwidth=2)
        solve_button.grid(row=0, column=0, padx=10, pady=5, ipadx=10)

        # Clear button
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_board, font=('Arial', 14, 'bold'),
                                 bg="#FF5252", fg="white", relief="raised", borderwidth=2)
        clear_button.grid(row=0, column=1, padx=10, pady=5, ipadx=10)

        # Hint button (only if a random puzzle was generated)
        if self.generate_random:
            hint_button = tk.Button(button_frame, text="Hint", command=self.give_hint, font=('Arial', 14, 'bold'),
                                    bg="#FFD700", fg="black", relief="raised", borderwidth=2)
            hint_button.grid(row=0, column=2, padx=10, pady=5, ipadx=10)

        # Back button
        back_button = tk.Button(button_frame, text="Back", command=self.back_to_initial, font=('Arial', 14, 'bold'),
                                bg="grey", fg="white", relief="raised", borderwidth=2)
        back_button.grid(row=0, column=3, padx=10, pady=5, ipadx=10)

    def generate_random_sudoku(self):
        """Fills the board with a predefined random Sudoku puzzle."""
        sample_puzzle = [
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
        # Populate the entries grid with sample puzzle values
        for i in range(9):
            for j in range(9):
                if sample_puzzle[i][j] != 0:
                    self.entries[i][j].insert(0, str(sample_puzzle[i][j]))
                    self.entries[i][j].config(state="disabled", fg="blue")

    def solve_sudoku(self):
        """Attempts to solve the Sudoku puzzle using backtracking."""
        # Populate the grid with values from the entry boxes
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.grid[i][j] = int(value) if value.isdigit() else 0

        if self.solve():
            self.update_board()
            messagebox.showinfo("Success", "Sudoku solved successfully!")
        else:
            messagebox.showerror("Error", "No solution exists.")

    def solve(self):
        """Backtracking algorithm to solve the Sudoku puzzle."""
        empty_cell = self.find_empty_location()

        if not empty_cell:
            return True  # Puzzle solved

        row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                self.grid[row][col] = 0  # Backtrack if no solution

        return False

    def find_empty_location(self):
        """Finds the next empty cell in the grid."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        """Checks if placing a number in the given cell is valid."""
        # Check row and column for conflicts
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False

        # Check 3x3 subgrid for conflicts
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def update_board(self):
        """Displays the solved Sudoku puzzle on the board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(tk.END, str(self.grid[i][j]))
                self.entries[i][j].config(fg="blue")

    def clear_board(self):
        """Clears the entire Sudoku board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(fg="black")
                self.grid[i][j] = 0

    def give_hint(self):
        """Provides a hint by filling one random empty cell with the correct value."""
        # Store current grid state and solve the puzzle
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.grid[i][j] = int(value) if value.isdigit() else 0

        temp_grid = [row[:] for row in self.grid]
        if self.solve():
            empty_cells = [(i, j) for i in range(9)
                           for j in range(9) if self.entries[i][j].get() == '']
            if empty_cells:
                i, j = random.choice(empty_cells)
                hint_value = self.grid[i][j]
                self.entries[i][j].insert(0, str(hint_value))
                self.entries[i][j].config(fg="green")

            # Restore the original unsolved grid
            self.grid = temp_grid
        else:
            messagebox.showerror("Error", "No solution exists.")

    def back_to_initial(self):
        """Returns to the initial window by closing the current window."""
        self.master.destroy()
        main()  # Reopens the initial window


def open_solver(generate_random=False):
    root = tk.Tk()
    app = SudokuSolver(root, generate_random=generate_random)
    root.mainloop()


def main():
    # Create the initial window
    initial_window = tk.Tk()
    initial_window.title("Sudoku Solver Options")
    initial_window.geometry("400x300")  # Set window size
    initial_window.config(bg="lightgrey")

    # Frame for padding and centering
    frame = tk.Frame(initial_window, bg="lightgrey")
    frame.pack(expand=True)

    # Title label
    label = tk.Label(
        frame,
        text="Choose an Option",
        font=('Arial', 18, 'bold'),
        bg="lightgrey",
        fg="black"
    )
    label.pack(pady=(0, 20))

    # Button for user input puzzle
    user_input_button = tk.Button(
        frame,
        text="Input Your Own Puzzle",
        font=('Arial', 14),
        bg="lightblue",
        activebackground="skyblue",
        width=20,
        command=lambda: (initial_window.destroy(),
                         open_solver(generate_random=False))
    )
    user_input_button.pack(pady=10)

    # Button for generating random puzzle
    random_button = tk.Button(
        frame,
        text="Generate Random Puzzle",
        font=('Arial', 14),
        bg="lightgreen",
        activebackground="lightgreen",
        width=20,
        command=lambda: (initial_window.destroy(),
                         open_solver(generate_random=True))
    )
    random_button.pack(pady=10)

    # Start the main loop
    initial_window.mainloop()


# Run the main function to start the application
main()
