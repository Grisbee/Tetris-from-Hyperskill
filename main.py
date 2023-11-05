import numpy as np

# creating the grid with dimensions received from the user
grid_length, grid_height = input().split(" ", 1)
grid_height = int(grid_height)
grid_length = int(grid_length)

grid = np.full(grid_height * grid_length, "-")
start = int(int(grid_length) / 2 - 2)

grid = grid.reshape(grid_height, grid_length)
current_grid = np.array(grid)


# piece configuration
O = [[[0, 1], [0, 2], [1, 1], [1, 2]]] * 5

I = [[[0, 1], [1, 1], [2, 1], [3, 1]],
     [[0, 0], [0, 1], [0, 2], [0, 3]],
     [[0, 1], [1, 1], [2, 1], [3, 1]],
     [[0, 0], [0, 1], [0, 2], [0, 3]],
     [[0, 1], [1, 1], [2, 1], [3, 1]]]

S = [[[0, 1], [0, 2], [1, 0], [1, 1]],
     [[0, 1], [1, 1], [1, 2], [2, 2]],
     [[0, 1], [0, 2], [1, 0], [1, 1]],
     [[0, 1], [1, 1], [1, 2], [2, 2]],
     [[0, 1], [0, 2], [1, 0], [0, 1]]]

Z = [[[0, 1], [0, 2], [1, 2], [1, 3]],
     [[0, 2], [1, 1], [1, 2], [2, 1]],
     [[0, 1], [0, 2], [1, 2], [1, 3]],
     [[0, 2], [1, 1], [1, 2], [2, 1]],
     [[0, 1], [0, 2], [1, 2], [1, 3]]]

L = [[[0, 1], [1, 1], [2, 1], [2, 2]],
     [[0, 2], [1, 0], [1, 1], [1, 2]],
     [[0, 1], [0, 2], [1, 2], [2, 2]],
     [[1, 0], [1, 1], [1, 2], [2, 0]]]

J = [[[0, 2], [1, 2], [2, 1], [2, 2]],
     [[0, 0], [0, 1], [0, 2], [1, 2]],
     [[0, 1], [0, 2], [1, 1], [2, 1]],
     [[0, 1], [1, 1], [1, 2], [1, 3]]]

T = [[[0, 1], [1, 1], [1, 2], [2, 1]],
     [[0, 1], [1, 0], [1, 1], [1, 2]],
     [[0, 2], [1, 1], [1, 2], [2, 2]],
     [[0, 1], [0, 2], [0, 3], [1, 2]]
     ]

blocks = {
    "O": O,
    "I": I,
    "S": S,
    "Z": Z,
    "L": L,
    "J": J,
    "T": T
}


# function for printing the created grid
def print_grid(printed_grid):

    for b in range(grid_height):

        for c in range(grid_length):
            print(' '.join(map(str, printed_grid[b][c])), end="")
            if c < grid_length - 1:
                print(" ", end="")
        print()
    print()


def piece_length_right(piece, piece_rotation):
    length_value = [value[1] for value in piece[piece_rotation]]
    return max(length_value) + 1


def piece_length_left(piece, piece_rotation):
    length_value = [value[1] for value in piece[piece_rotation]]
    return min(length_value)


def piece_height(piece, piece_rotation):
    height_value = [value[0] for value in piece[piece_rotation]]
    return max(height_value) + 1


def check_for_rotation(piece, piece_rotation):
    if piece_rotation == 3:
        piece_rotation = -1
    right_space = start + position + piece_length_left(piece, piece_rotation + 1)
    left_space = start + position + piece_length_left(piece, piece_rotation + 1)
    if right_space < grid_length and left_space >= 0:
        return True
    else:
        return False


def check_underneath(symbol, block_rotation, height, position):
    for c in range(4):
        height_coord = symbol[block_rotation][c][0] + height + 1
        length_coord = symbol[block_rotation][c][1] + position + start
        if grid[height_coord][length_coord] == '0':
            return False
    return True


def create_grid(symbol, block_rotation, height, position):
    current_grid = np.array(grid)

    for a in range(4):
        height_coord = symbol[block_rotation][a][0] + height
        length_coord = symbol[block_rotation][a][1] + position + start

        current_grid[height_coord][length_coord] = "0"
    if should_print == True:
        print_grid(current_grid)
    return current_grid


print_grid(grid)
command = ""
block = ""
should_print = True

while command != "exit":
    print("insert a command")
    command = str(input())
    if command == "piece":
        print("insert the type of block you want to use")
        block = str(input())
    elif command == "break":
        full_rows = 0
        for p in range(grid_height):
            if '-' not in grid[p]:
                full_rows += 1

        for d in range(grid_height - 1, full_rows, -1):
            # print(grid[d])
            # print(grid[d-full_rows])
            grid[d] = grid[d - full_rows]
        print()
        print_grid(grid)
        continue
    elif command == "down":
        print_grid(grid)
        continue
    elif command == "exit":
        break
    rotation, height, position = 0, 0, 0
    should_print = True
    command = ""
    if block in blocks:
        create_grid(blocks[block], rotation, height, position)

    while command != "stop":

        if height + piece_height(blocks[block], rotation) < grid_height and check_underneath(blocks[block], rotation, height, position) == True:
            command = str(input())
            if command == "down":
                height += 1
                create_grid(blocks[block], rotation, height, position)
            elif command == "left":
                if start + position + piece_length_left(blocks[block], rotation) > 0:
                    position -= 1
                height += 1
                create_grid(blocks[block], rotation, height, position)
            elif command == "right":
                if start + position + piece_length_right(blocks[block], rotation) < grid_length:
                    position += 1
                height += 1
                create_grid(blocks[block], rotation, height, position)
            elif command == "rotate":
                if check_for_rotation(blocks[block], rotation):
                    if rotation == 3:
                        rotation = -1
                    rotation += 1
                height += 1
                create_grid(blocks[block], rotation, height, position)
            elif command == "exit":
                break
        else:
            should_print = False
            grid = np.array(create_grid(blocks[block], rotation, height, position))
            if '0' in grid[0]:
                temporary_input = input()
                print_grid(grid)
                print("Game Over!")
                command = "exit"
                break
            command = "stop"
            break
