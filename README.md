# Sudoku Solver

This is a graphical application to solve Sudoku puzzles. It provides an interface to input a custom Sudoku puzzle or generate a random puzzle, then solves it using a backtracking algorithm. This application is built with Python and uses the Tkinter library for its GUI.

## Features

- *Custom Puzzle Input*: Manually enter a Sudoku puzzle and solve it.
- *Random Puzzle Generator*: Generate a random Sudoku puzzle to solve.
- *Hint Feature*: Provides a hint by filling one empty cell.
- *Clear and Reset*: Clear the board to start over with a new puzzle.
- *User-Friendly Interface*: Simple and interactive UI with buttons to control the puzzle board.

## How It Works

The Sudoku Solver uses a backtracking algorithm to solve the puzzle:
1. It finds empty cells in the grid.
2. For each empty cell, it tries numbers 1-9, checking for validity.
3. If a valid number is found, it proceeds; if not, it backtracks.

## Installation

1. *Clone the repository*:
   ```bash
   git clone https://github.com/Ordinary-droid/sudoku_solver
2. *Navigate to the repository*:
   ```bash
   cd sudoku_solver
3. *Run the code*:
   ```bash
   python sudoku_solver.py
