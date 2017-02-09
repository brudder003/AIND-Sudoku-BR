import numpy as np

# SETTING UP THE BOARD
# record rows/cols as strings
rows = 'ABCDEFGHI'
cols = '123456789'


# helper function we'll use to get a list boxes
def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]


# create that list of all boxes
boxes = cross(rows, cols)

# similarly, we want a list of all row, col and 3x3 square
# each item in the list is a list itself, of boxes
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# NEW FOR THE PROJECT
#treat diagonals like units too!
boxes_array = np.asarray(row_units)
diagonal_unit1 = list(boxes_array.diagonal())
diagonal_unit2 = list(np.diag(np.rot90(boxes_array)))


# create a list of all units
# append the indiv unit lists together one after the other
unitlist = row_units + column_units + square_units
unitlist.append(diagonal_unit1)
unitlist.append(diagonal_unit2)

# dict keys are boxes, 3 vals per key which are a list of the row, col
# and 3x3 associate with each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# dict keys are boxes, 1 val per key, which is a set containing all
# peers of a given box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# initialize so append works in assign_values
assignments = []


# helper function for assigning values
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.

    Brett's strategy: 1.)loop over unit list, turn each unit into a dict where
    keys are boxes and values are nums (as string) avail to that sudoku box
    2.) flip that dict created for each unit so nums are keys and vals are box labels
    then if the key of the flipped dict has length 2 and there are 2 values then we found a twin
    3.)for all twins loop over the two numbers and eliminate them from all other boxes
    in that unit, return as described above.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # after = values.copy() -- don't need in final, used in dev.

    # loop over units
    for unit in unitlist:
        # create a dict where keys are boxes and values are from the 'values' dict for that box
        vals_this_unit = []
        for u in unit:
            vals_this_unit.append(values[u])
        dict_this_unit = dict(zip(unit, vals_this_unit))

        # flip dict_this_unit so 'values' are keys with box labels as values
        # this is so any repeated 'value' will have multiple values (box labels)
        flipped_dict = {}
        for key, value in dict_this_unit.items():
            if value not in flipped_dict:
                flipped_dict[value] = [key]
            else:
                flipped_dict[value].append(key)

        # filter for where the length of key and number of values are both two
        # this leaves us with just a dict of twins in the same unit
        flipped_dict_twins = dict((key, value) for key, value in flipped_dict.items() \
                                  if len(key) == 2 and len(value) == 2)
        # unit_reduce = unit.copy() -- don't need in final used in dev.

        # iter over keys, vals in flipped dict twins (recall we are in one unit)
        # unit reduce so we dont change the values of twins themselves
        # then iter over the two values of the twin and remove them from all other boxes in the unit
        for key, value in flipped_dict_twins.items():
            unit_reduce = list(set(unit) - set(value))

            for char in key:
                for unit_red in unit_reduce:
                    values[unit_red] = values[unit_red].replace(char, '')
    return values

# this stays the same from the lesson
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

# this stays the same from the lesson
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# this stays the same from the lesson
def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

# this stays the same from the lesson
def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value
    to this box. Input: A sudoku in dictionary form. Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

# this stays the same from the lesson, except added the naked twins strategy
# thinking naked twins will be most useful after eliminate
def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        assignments.append(values.copy())
        values = eliminate(values)
        assignments.append(values.copy())
        # Use naked twins strategy
        values = naked_twins(values)
        assignments.append(values.copy())
        # Use the Only Choice Strategy
        values = only_choice(values)
        assignments.append(values.copy())
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    pass


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.

    Using depth-first search and propagation, try all possible values."""
    # First, reduce the puzzle using the previous function
    values = grid_values(grid)
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(solve(grid2))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
