import time
from pathlib import Path

FREE_SPACE = "free space"
FILE = "file"
STATES = [FILE, FREE_SPACE]
CURR_STATE = 0


def change_state():
    global CURR_STATE
    CURR_STATE = (CURR_STATE + 1) % len(STATES)


def add_block_repr(block_repr_list, file_id, disk_item_len):
    if disk_item_len == 0:
        return
    list_of_repr = []
    for _ in range(disk_item_len):
        list_of_repr.append(f"{file_id}")
    block_repr_list.append(list_of_repr)


def get_block_repr(disk_map):
    block_repr_list = []
    file_id = 0
    for disk_item_len in disk_map:
        if STATES[CURR_STATE] == FILE:
            add_block_repr(block_repr_list, file_id, int(disk_item_len))
            file_id += 1
        else:
            add_block_repr(block_repr_list, ".", int(disk_item_len))
        change_state()
    return block_repr_list


def swap_frag(blocks_list, end_frag_ind, insert_ind):
    file_frag = blocks_list[end_frag_ind]
    free_frag = blocks_list[insert_ind]

    # Move the file up
    blocks_list[insert_ind] = file_frag

    extra_dots = len(free_frag) - len(file_frag)

    # Used to update "excluding the end blocks we've already seen"
    replacing_from_the_end = len(blocks_list) - end_frag_ind - 1

    # Move the remaining dots to the end
    new_end_frag = free_frag[: len(free_frag) - extra_dots]
    try:
        if "." in blocks_list[end_frag_ind + 1]:
            new_end_frag.extend(blocks_list[end_frag_ind + 1])
            del blocks_list[end_frag_ind + 1]
            replacing_from_the_end -= 1
    except IndexError:
        pass
    if "." in blocks_list[end_frag_ind - 1]:
        blocks_list[end_frag_ind - 1].extend(new_end_frag)
        del blocks_list[end_frag_ind]
    else:
        blocks_list[end_frag_ind] = new_end_frag

    # Place the extra dots that fit with the file
    if extra_dots > 0:
        blocks_list.insert(insert_ind + 1, free_frag[:extra_dots])
    return replacing_from_the_end + 1


def defrag_blocks_list(blocks_list):
    list_changed = True

    # What block from the end we are looking at (so when our overall loop resets, we don't try to move a file we are done with)
    from_the_end_look = 0

    # Overall loop because if the list changes during an inner loop, we need to start over
    while list_changed:
        list_changed = False
        if from_the_end_look < 0:
            break

        # Loop from the end (excluding the end blocks we've already seen)
        for ind, frag in enumerate(
            blocks_list[: len(blocks_list) - from_the_end_look][::-1]
        ):

            # Get the read end ind of the overall (not excluding the end blocks we've already seen)
            end_ind = len(blocks_list) - 1 - ind - from_the_end_look
            if "." in frag:
                continue  # Free space, not a file to move up

            # Loop from beginning up to the file we are trying to move up
            for look_ind, look_frag in enumerate(blocks_list[:end_ind]):
                if "." not in look_frag:
                    continue  # File, not free space we can move the file into
                if len(look_frag) < len(frag):
                    continue  # Free space not big enough
                from_the_end_look = swap_frag(blocks_list, end_ind, look_ind)
                list_changed = True
                break
            if list_changed:
                break  # List changed, we need to start from the beginning

    return blocks_list


def get_checksum(blocks_list):
    checksum = 0
    ind = 0
    for block_list in blocks_list:
        if "." not in block_list:
            for internal_ind, block in enumerate(block_list):
                checksum += (ind + internal_ind) * int(block)
        ind += len(block_list)
    return checksum


def main():
    file_path = Path("input.txt")
    lines = file_path.read_text().splitlines()
    if len(lines) != 1:
        raise ValueError("Back input file")
    line = lines[0].strip()
    blocks_repr = get_block_repr(line)
    defragmented = defrag_blocks_list(blocks_repr)
    checksum = get_checksum(defragmented)
    print(f"{checksum = }")


if __name__ == "__main__":
    print("Start Solve")
    start = time.time()
    main()
    end = time.time()
    print("Done Solve")
    print(f"Took {end - start:.4f} seconds")
