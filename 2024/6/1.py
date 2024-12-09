CHARACTER = "^"
DIRECTIONS = ["up", "right", "down", "left"]
CURR_DIRECTION = 0


def turn():
    global CURR_DIRECTION
    global CHARACTER
    CURR_DIRECTION = (CURR_DIRECTION + 1) % len(DIRECTIONS)

    if DIRECTIONS[CURR_DIRECTION] == "up":
        CHARACTER = "^"
    elif DIRECTIONS[CURR_DIRECTION] == "right":
        CHARACTER = ">"
    elif DIRECTIONS[CURR_DIRECTION] == "down":
        CHARACTER = "V"
    else:  # Left
        CHARACTER = "<"


def move_forward(my_map, current_x, current_y):
    add_x = 0
    add_y = 0
    if DIRECTIONS[CURR_DIRECTION] == "up":
        add_y = -1
    elif DIRECTIONS[CURR_DIRECTION] == "right":
        add_x = 1
    elif DIRECTIONS[CURR_DIRECTION] == "down":
        add_y = 1
    else:  # Left
        add_x = -1

    potential_new_x = current_x + add_x
    potential_new_y = current_y + add_y

    if -1 in [potential_new_x, potential_new_y]:
        raise IndexError()

    if my_map[potential_new_y][potential_new_x] == "#":
        raise BaseException("Hitting obstacle")

    unique_move = 1
    if my_map[potential_new_y][potential_new_x] == "X":
        unique_move = 0

    # Place character
    my_map[potential_new_y] = (
        my_map[potential_new_y][:potential_new_x]
        + CHARACTER
        + my_map[potential_new_y][potential_new_x + 1 :]
    )

    # Mark spot
    my_map[current_y] = (
        my_map[current_y][:current_x] + "X" + my_map[current_y][current_x + 1 :]
    )
    return potential_new_x, potential_new_y, unique_move


def print_my_map(my_map):
    for line in my_map:
        print(line)


def main():
    with open("input.txt", "r") as fp:
        my_map = fp.readlines()
        my_map = [line.strip() for line in my_map]
    x_len = len(my_map[0])
    y_len = len(my_map)

    for ind_y, line in enumerate(my_map):
        for ind_x, box in enumerate(line):
            if box == CHARACTER:
                current_x = ind_x
                current_y = ind_y

    count = 1

    path = []
    while 0 <= current_x < x_len and 0 <= current_y < y_len:
        try:
            current_x, current_y, add_moved = move_forward(my_map, current_x, current_y)
            count += add_moved
            if (current_x, current_y, CURR_DIRECTION) in path:
                print(path)
                print(f"({current_x}, {current_y}, {CURR_DIRECTION})")
                input("Looping!!!!")
            path.append((current_x, current_y, CURR_DIRECTION))
        except IndexError:
            break
        except KeyboardInterrupt:
            print("")
            print_my_map(my_map)
            input("Completed move\n\n")
        except:
            turn()
    print(f"{count = }")


if __name__ == "__main__":
    main()
