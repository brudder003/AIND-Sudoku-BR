# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?

A: As stated in lesson 7 constraint propagation means using local constraints to reduce the search space. In
practice this is achieved by alternating between enforcing a constraint and eliminating choices.

In naked twins we have the local constraint that no other box in a unit where two boxes each have the same two values
(twins) can have either of the values in the twin boxes. By taking in in a board with lots of possibilities, then
applying the naked twins constraint through all the units, we are narrowing reducing the search space and
successfully applying constraint propagation to solve naked twins.

The propagation happens in an order, so multiple rounds of propagation through every unit could continue to reduce
the search space. We propagate over units until the problem is solved or we need an additional constraint (strategy)
to make further progress.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?

A: Using the same description of constraint as Question 1 (and lesson 7), we have the local constraint that the main
diagonals on the sudoku board must each contain the numbers 1 through 9. This is the same as the constraint we already
have for individual rows, columns and 3x3 squares (which are defined as units in lesson 3). We add a list of boxes from
each of main diagonals to list of constraints.

At this point we are already set up to propagate our 'eliminate', 'only choice', and 'naked twins' constraints across
all units. So by adding the diagonals to the list of units we are enforcing them as a constraint like any other unit
and propagating the their application by repeated application of these strategies until the game is solved or we need
and additional constraint to make further progress.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.