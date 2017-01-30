assignments = []


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
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    total_chars_on_board_before = sum([len(values[box]) for box in boxes])

    for unit in target_unit_list:
        box_sets = dict([(box, values[box]) for box in unit if len(values[box]) == 2])
        digits_container = set([value for value in box_sets.values() if list(box_sets.values()).count(value) == 2])
        for digits in digits_container:
            for digit in digits:
                change_target_boxes = [box for box in unit if
                                       values[box] not in digits_container and digit in values[box]]
                for box in change_target_boxes:
                    values = assign_value(values, box, values[box].replace(digit, ""))

    total_chars_on_board_after = sum([len(values[box]) for box in boxes])
    return naked_twins(values) if total_chars_on_board_after < total_chars_on_board_before else values


def cross(A, B):
    " Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = "123456789"

    for char in grid:
        chars.append(digits if char == '.' else char)

    assert len(chars) == 81

    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in values.keys())
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in "ABCDEFGHI":
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in "123456789"))
        if r in 'CF': print(line)
    print("\n\n")
    return


def eliminate(values):
    single_digit_boxes = [box for box in values.keys() if len(values[box]) == 1]

    for box in single_digit_boxes:
        for peer_box in peer_list[box]:
            if peer_box not in single_digit_boxes and len(values[peer_box]) > 1:
                value = values[box]
                values = assign_value(values, peer_box, values[peer_box].replace(value, ""))

    return values


def only_choice(values):
    target_list = target_unit_list

    for unit in target_list:
        for digit in "123456789":
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)

    return values


def reduce_puzzle(values):
    finished = False

    while not finished:
        previous = sum([len(values[box]) for box in values.keys()])

        values = eliminate(values)

        if all(len(values[box]) == 1 for box in boxes):
            if is_completed(values):
                return values

        values = only_choice(values)

        if all(len(values[box]) == 1 for box in boxes):
            if is_completed(values):
                return values

        values = naked_twins(values)

        if all(len(values[box]) == 1 for box in boxes):
            if is_completed(values):
                return values

        after = sum([len(values[box]) for box in values.keys()])

        finished = previous == after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    values = reduce_puzzle(values)

    if values is False:
        return False

    if is_completed(values):
        return values
    elif all(len(values[box]) == 1 for box in boxes):
        return False

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for char in values[s]:
        new_values = values.copy()
        new_values[s] = char
        attempt = search(new_values)
        if attempt:
            return attempt


def create_diagonal_units():
    first_unit = []
    second_unit = []
    for i in range(len(rows)):
        first_unit.append(rows[i] + cols[i])
        second_unit.append(rows[len(rows) - i - 1] + cols[i])
    return [first_unit, second_unit]


def peers(box):
    _peers = []
    for unit in target_unit_list:
        if box in unit:
            _peers += unit

    _my_set = set(_peers)
    _my_set.discard(box)
    return list(_my_set)


def is_completed(values):
    # target_list = unit_list
    target_list = target_unit_list
    #     for each row only has 1 and only one
    for unit in target_list:
        temp_set = set()
        for box in unit:
            if len(values[box]) is not 1:
                return False
            if values[box] in temp_set:
                return False
            temp_set.add(values[box])
    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sodoku_boxes = grid_values(grid)

    solution = search(sodoku_boxes)

    if solution:
        return solution
    else:
        raise Exception('No Solution Found!')


rows = "ABCDEFGHI"
cols = "123456789"

# This are some constants
col_units = [cross(rows, col) for col in cols]
row_units = [cross(row, cols) for row in rows]
square_unit = [cross(row, col) for row in (["ABC", "DEF", "GHI"]) for col in (["123", "456", "789"])]
diagonal_units = create_diagonal_units()
boxes = cross(rows, cols)
standard_unit_list = col_units + row_units + square_unit
diagonal_unit_list = standard_unit_list + diagonal_units

# The target list is for toggle between diagonal or standard sudoku
target_unit_list = diagonal_unit_list
peer_list = dict([(box, peers(box)) for box in boxes])

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
