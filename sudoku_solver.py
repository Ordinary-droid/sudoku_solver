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
        """Generates a random Sudoku puzzle."""

        base = 3
        side = base * base

        def fill_box(row):
            """Fill a box with random numbers."""
            nums = list(range(1, base * base + 1))
            random.shuffle(nums)
            for i in range(base):
                for j in range(base):
                    self.grid[row + i][row + j] = nums[i * base + j]

        def fill_diagonal():
            """Fill the diagonal boxes."""
            for i in range(base):
                fill_box(i * base)

        def is_valid(num, row, col):
            """Check if a number can be placed at grid[row][col]."""
            for x in range(9):
                if self.grid[row][x] == num or self.grid[x][col] == num:
                    return False

            start_row = row - row % base
            start_col = col - col % base
            for i in range(base):
                for j in range(base):
                    if self.grid[i + start_row][j + start_col] == num:
                        return False

            return True

        def fill_remaining(row, col):
            """Fill remaining cells using backtracking."""
            if col >= side:  # Move to next row
                col = 0
                row += 1
            if row >= side:  # If we filled all rows
                return True

            if self.grid[row][col] != 0:  # Skip filled cells
                return fill_remaining(row, col + 1)

            for num in range(1, base * base + 1):
                if is_valid(num, row, col):
                    self.grid[row][col] = num
                    if fill_remaining(row, col + 1):  # Recursion to fill next cell
                        return True

            self.grid[row][col] = 0  # Backtrack
            return False

        fill_diagonal()

        fill_remaining(0, 0)  # Fill remaining cells

        # Randomly remove some numbers to create a puzzle
        def unfill():
            count = random.randint(40, 60)  # Number of cells to remove
            while count > 0:
                i = random.randint(0, side - 1)
                j = random.randint(0, side - 1)
                if self.grid[i][j] != 0:
                    self.grid[i][j] = 0
                    count -= 1

        unfill()

        # Update entries with the generated puzzle
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(state="disabled", fg="blue")

    def solve_sudoku(self):
        """Extracts values from entries and tries to solve the Sudoku."""
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
            return True  # Solved

        row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                self.grid[row][col] = 0  # Backtrack

        return False

    def find_empty_location(self):
        """Finds an empty cell in the grid."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        """Checks if a number can be placed in a specific cell."""
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def update_board(self):
        """Updates the GUI with the solved Sudoku board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(tk.END, str(self.grid[i][j]))
                self.entries[i][j].config(fg="blue")

    def clear_board(self):
        """Clears the Sudoku board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(fg="black")
                self.grid[i][j] = 0

    def give_hint(self):
        """Provide a hint by filling one empty cell with a correct number."""
        empty_cells = [(i, j) for i in range(9)
                       for j in range(9) if self.entries[i][j].get() == '']
        if not empty_cells:
            messagebox.showinfo("Hint", "No empty cells available.")
            return

        # Solve the puzzle to get a solution.
        temp_grid = [row[:] for row in self.grid]
        if not self.solve():
            messagebox.showerror("Error", "No solution exists.")
            return

        # Choose a random empty cell and fill it with a hint value.
        i, j = random.choice(empty_cells)
        hint_value = self.grid[i][j]
        self.entries[i][j].insert(0, str(hint_value))
        self.entries[i][j].config(fg='green')

        # Restore original grid state.
        self.grid = temp_grid

    def back_to_initial(self):
        """Close current window and return to the initial window."""
        self.master.destroy()
        main()


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
