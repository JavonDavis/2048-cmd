LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


def empty_slots(game_grid):
    """Made this abstract in case I wanted to change the size of the grid """
    return [(x, y) for x in xrange(len(game_grid)) for y in xrange(len(game_grid[x])) if game_grid[x][y] == 0]


def random_position(game_grid):
    """Returns a random empty position in the grid """
    from random import choice
    return choice(empty_slots(game_grid))


def random_number():
    from random import choice
    return choice([2] * 96 + [4] * 4)


def add_random_number(game_grid):
    row, column = random_position(grid)
    game_grid[row][column] = random_number()


def update(game_grid, row, column, direction, can_merge):
    """Updates the the grid based on the value at row, column and the direction"""
    # can_merge solves the problem I left for the kids to identify in the gui version
    num1 = game_grid[row][column]
    if direction == UP and row > 0:
        new_row, new_column = row - 1, column
    elif direction == DOWN and row < 3:
        new_row, new_column = row + 1, column
    elif direction == RIGHT and column < 3:
        new_row, new_column = row, column + 1
    elif direction == LEFT and column > 0:
        new_row, new_column = row, column - 1
    else:
        return
    if game_grid[new_row][new_column] == 0:
        game_grid[new_row][new_column] = num1
        game_grid[row][column] = 0
        return update(game_grid, new_row, new_column, direction, can_merge)
    elif can_merge and game_grid[new_row][new_column] == game_grid[row][column]:
        game_grid[new_row][new_column] = num1 * 2
        game_grid[row][column] = 0
        return update(game_grid, new_row, new_column, direction, False)
    return


def update_grid(game_grid, direction):
    """Calls the appropriate function to update the grid based on the direction"""
    if direction == LEFT:
        """Updates the grid for the leftward movement"""
        for row in xrange(len(game_grid)):
            for column in xrange(len(game_grid[row])):
                if game_grid[row][column] != 0:
                    update(game_grid, row, column, LEFT, True)

    elif direction == RIGHT:
        """Updates the grid for the rightward movement"""
        for row in xrange(len(game_grid)):
            for column in xrange(len(game_grid[row]) - 1, -1, -1):
                if game_grid[row][column] != 0:
                    update(game_grid, row, column, RIGHT, True)
    elif direction == DOWN:
        """Updates the grid for the downward movement"""
        for row in xrange(len(game_grid) - 1, -1, -1):
            for column in xrange(len(game_grid[row])):
                if game_grid[row][column] != 0:
                    update(game_grid, row, column, DOWN, True)
    elif direction == UP:
        """Updates the grid for the upward movement"""
        for row in xrange(len(game_grid)):
            for column in xrange(len(game_grid[row])):
                if game_grid[row][column] != 0:
                    update(game_grid, row, column, UP, True)
    else:
        raise Exception("Invalid direction received ensure UP, LEFT, DOWN and RIGHT "
                        "are defined with unique integer values")


if __name__ == "__main__":
    """
    Representing the game board as a list of lists
    where a 0 would represent an empty position on the board.
    Starts off with an empty board
    """

    raw_input("Welcome to Command Line 2048, Press any key to begin!")

    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

    # Start the game by placing two random numbers in the grid
    add_random_number(grid)
    add_random_number(grid)

    while True:
        for item in grid:
            print item
        choice = int(raw_input("Enter direction to move(LEFT=0, RIGHT=1, UP =2, DOWN = 3, 4 to stop the game)\n"))

        if choice == 4:
            break

        if choice in xrange(0, 4):
            from copy import deepcopy

            old_state = deepcopy(grid)
            update_grid(grid, choice)

            if old_state != grid:
                add_random_number(grid)
        else:
            print "Not a valid move!"
            continue

        for rowElement in grid:
            for number in rowElement:
                if number == 2048:
                    print "You win! Congrats!"
                    break

        if not empty_slots(grid):
            for i in xrange(len(grid)):
                for j in xrange(len(grid[i])):
                    num = grid[i][j]
                    if i > 0:
                        if grid[i - 1][j] == num:
                            continue
                    if i < 3:
                        if grid[i + 1][j] == num:
                            continue
                    if j > 0:
                        if grid[i][j - 1] == num:
                            continue
                    if j < 3:
                        if grid[i][j + 1] == num:
                            continue
        else:
            continue
        print "You lose! Sorry!"
