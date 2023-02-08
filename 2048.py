from random import choice

# options
width = 4
starting_blocks = 2
starting_value = 2

grid = {}

for x in range(width):
    for y in range(width):
        grid.update({(x, y): 0})


def is_occupied(xy):
    """Returns True when provided xy is filled, False if empty."""
    return grid.get(xy) != 0


def get_occupied_spaces():
    """Returns a tuple of all filled coordinate-tuples on the board."""
    return tuple(filter(is_occupied, grid))


def is_empty(xy):
    """Returns True when provided xy is empty, False if filled."""
    return not is_occupied(xy)


def get_empty_spaces():
    """Returns a tuple of all empty coordinate-tuples on the board."""
    return tuple(filter(is_empty, grid))


def assign(xy, value):
    """Assigns a value to a coordinate-tuple in the grid. Returns grid."""
    return grid.update({xy: value})


def get_next_spaces(xy, direction):
    """Returns a list containing all spaces in the specified direction. Excludes provided xy."""
    spaces = [xy]

    for idx in range(width):
        latest = spaces[-1]
        next_x = latest[0] + direction[0]
        next_y = latest[1] + direction[1]

        if (next_x >= width or next_x < 0) or (next_y >= width or next_y < 0):  # stay within bounds
            return spaces[1:]  # exclude provided xy

        spaces.append((next_x, next_y))


def populate():
    """Populates the starting area with a square with value starting_value."""
    assign(choice(get_empty_spaces()), starting_value)


def print_grid():
    """Prints the grid to the terminal."""
    spacing = len(str(max(grid.values())))

    for y in range(width):
        row = ""
        for x in range(width):
            value = grid.get((x, y))
            distance = spacing - len(str(value)) + 1

            row += str(grid.get((x, y))) + (distance * " ")

        print(row)


def letter_to_direction(letter):
    """Returns tuple which represents the x,y direction and preferred update dir, based on the user-provided letter."""
    normal = range(0, width)
    reverse = reversed(normal)

    match letter.lower():
        case "w":  # up
            return (0, -1), ("y", normal, normal)
        case "s":  # down
            return (0, 1), ("y", normal, reverse)
        case "a":  # left
            return (-1, 0), ("x", normal, normal)
        case "d":  # right
            return (1, 0), ("x", reverse, normal)
        case invalid:
            print(f"Unknown direction: {invalid}, try again.")
            return None


def main():
    global grid
    for _ in range(starting_blocks):
        populate()

    print("Welcome to py2048!",
          "Goal: get a score of 2048",
          "Controls:",
          "- w: up",
          "- s: down",
          "- a: left",
          "- d: right",
          sep="\n")

    score = 0

    while len(get_empty_spaces()) > 0:
        print()
        print(f"Score: {score}")
        print()
        print_grid()
        print()

        direction_data = letter_to_direction(input())

        if direction_data is None:
            continue  # don't ruin progress if they enter incorrect letter

        direction = direction_data[0]
        preference = direction_data[1]

        total = []

        # ensure updating happens in the correct direction to avoid goofiness
        if preference[0] == "x":
            for x in preference[1]:
                for y in preference[2]:
                    total.append((x, y))
        else:
            for y in preference[2]:
                for x in preference[1]:
                    total.append((x, y))

        occupied = list(filter(is_occupied, total))

        for xy in occupied:
            next_spaces = get_next_spaces(xy, direction)

            if len(next_spaces) == 0:
                continue

            next_occupied = tuple(filter(is_occupied, next_spaces))

            current_value = grid.get(xy)

            if len(next_occupied) > 0:
                first = next_occupied[0]

                if grid.get(first) == current_value:
                    # merge
                    grid[xy] = 0
                    grid[first] = current_value * 2

                    score += current_value * 2

                    continue

                # can't merge
                new_xy = (first[0] - direction[0], first[1] - direction[1])
                grid[xy] = 0
                grid[new_xy] = current_value
                continue

            # no obstacles
            grid[xy] = 0
            grid[next_spaces[-1]] = current_value

        populate()


if __name__ == '__main__':
    main()
