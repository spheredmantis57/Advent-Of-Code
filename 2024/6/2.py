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
    return potential_new_x, potential_new_y


def print_my_map(my_map):
    for line in my_map:
        print(line)


import time


def main():
    global CHARACTER
    global CURR_DIRECTION
    with open("input.txt", "r") as fp:
        my_map = fp.readlines()
        my_map = [line.strip() for line in my_map]
    x_len = len(my_map[0])
    y_len = len(my_map)

    # Save original map
    good_map = my_map.copy()

    for ind_y, line in enumerate(my_map):
        for ind_x, box in enumerate(line):
            if box == CHARACTER:
                current_x = ind_x
                current_y = ind_y
    start_x = current_x
    start_y = current_y

    loop_count = 0

    path_taken = set()
    while 0 <= current_x < x_len and 0 <= current_y < y_len:
        try:
            current_x, current_y = move_forward(my_map, current_x, current_y)
            path_taken.add((current_x, current_y))
        except IndexError:
            break
        except:
            turn()

    for ind_x, ind_y in path_taken:
        # Reset map
        # my_map = good_map.copy()
        CURR_DIRECTION = 0
        turns = []
        CHARACTER = "^"

        current_x = start_x
        current_y = start_y
        my_map[ind_y] = my_map[ind_y][:ind_x] + "#" + my_map[ind_y][ind_x + 1 :]
        while 0 <= current_x < x_len and 0 <= current_y < y_len:
            try:
                current_x, current_y = move_forward(my_map, current_x, current_y)
            except IndexError:
                break
            except:
                turn()
                if (current_x, current_y, CURR_DIRECTION) in turns:
                    loop_count += 1
                    break
                turns.append((current_x, current_y, CURR_DIRECTION))
        my_map[ind_y] = my_map[ind_y][:ind_x] + "." + my_map[ind_y][ind_x + 1 :]
    print(f"{loop_count = }")


if __name__ == "__main__":
    print("Start Solve")
    start = time.time()
    main()
    end = time.time()
    print("Done Solve")
    print(f"Took {end - start:.4f} seconds")
