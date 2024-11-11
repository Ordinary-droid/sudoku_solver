import tkinter as tk
from tkinter import messagebox
import random


class SudokuSolver:
    def __init__(self, master, generate_random=False):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.config(bg="lightgrey")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.generate_random = generate_random  # Track if random puzzle is chosen

        self.create_widgets()

        if generate_random:
            self.generate_random_sudoku()

    def create_widgets(self):
        # Configure grid weights for responsive design
        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

        # Create the grid of entry boxes
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.master, font=('Arial', 18), justify='center', borderwidth=2, relief="solid")
                entry.grid(row=i, column=j, sticky="nsew", padx=(1, 1 if (j + 1) % 3 != 0 else 5),
                           pady=(1, 1 if (i + 1) % 3 != 0 else 5))
                self.entries[i][j] = entry

        # Create Solve button
        solve_button = tk.Button(self.master, text="Solve", command=self.solve_sudoku, font=('Arial', 14), bg="lightblue", fg="black", relief="raised", borderwidth=2)
        solve_button.grid(row=10, column=1, columnspan=3, pady=10, sticky="ew")

        # Create Clear button
        clear_button = tk.Button(self.master, text="Clear", command=self.clear_board, font=('Arial', 14), bg="lightcoral", fg="black", relief="raised", borderwidth=2)
        clear_button.grid(row=10, column=5, columnspan=3, pady=10, sticky="ew")

        # Conditionally add the Hint button only if the puzzle is randomly generated
        if self.generate_random:
            hint_button = tk.Button(self.master, text="Hint", command=self.give_hint, font=('Arial', 14), bg="lightgreen", fg="black", relief="raised", borderwidth=2)
            hint_button.grid(row=11, column=1, columnspan=7, pady=10, sticky="ew")

        # Add Back button
        back_button = tk.Button(self.master, text="Back", command=self.back_to_initial, font=('Arial', 14), bg="grey", fg="black", relief="raised", borderwidth=2)
        back_button.grid(row=12, column=1, columnspan=7, pady=10, sticky="ew")

    def generate_random_sudoku(self):
        """Generates a random Sudoku puzzle."""
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
        for i in range(9):
            for j in range(9):
                if sample_puzzle[i][j] != 0:
                    self.entries[i][j].insert(0, str(sample_puzzle[i][j]))
                    self.entries[i][j].config(state="disabled", fg="blue")

    def solve_sudoku(self):
        """Extracts values from entries, tries to solve the Sudoku, and updates the board."""
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
        # Store the current grid state
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.grid[i][j] = int(value) if value.isdigit() else 0

        # Solve the puzzle to get a solution
        temp_grid = [row[:] for row in self.grid]
        if self.solve():
            empty_cells = [(i, j) for i in range(9)
                           for j in range(9) if self.entries[i][j].get() == '']
            if empty_cells:
                i, j = random.choice(empty_cells)
                hint_value = self.grid[i][j]
                self.entries[i][j].insert(0, str(hint_value))
                self.entries[i][j].config(fg="green")

            # Restore the original grid
            self.grid = temp_grid
        else:
            messagebox.showerror("Error", "No solution exists.")

    def back_to_initial(self):
        """Close current window and return to the initial window."""
        self.master.destroy()
        main()  # Reopen the initial window


def open_solver(generate_random=False):
    root = tk.Tk()
    app = SudokuSolver(root, generate_random=generate_random)
    root.mainloop()


def main():
    initial_window = tk.Tk()
    initial_window.title("Sudoku Solver Options")
    initial_window.config(bg="lightgrey")

    label = tk.Label(initial_window, text="Choose an option",
                     font=('Arial', 16), bg="lightgrey")
    label.pack(pady=20)

    user_input_button = tk.Button(initial_window, text="Input Your Own Puzzle",
                                  font=('Arial', 14), bg="lightblue", command=lambda: (initial_window.destroy(), open_solver(generate_random=False)))
    user_input_button.pack(pady=10)

    random_button = tk.Button(initial_window, text="Generate Random Puzzle",
                              font=('Arial', 14), bg="lightgreen", command=lambda: (initial_window.destroy(), open_solver(generate_random=True)))
    random_button.pack(pady=10)

    initial_window.mainloop()


if __name__ == "__main__":
    main()
