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
    for _ in range(disk_item_len):
        block_repr_list.append(f"{file_id}")


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


def defrag_blocks_list(blocks_list):
    end_ind = len(blocks_list) - 1
    for ind, frag in enumerate(blocks_list):
        if frag != ".":
            continue
        while blocks_list[end_ind] == ".":
            if not end_ind > ind:
                return blocks_list[: end_ind + 1]
            end_ind -= 1
        blocks_list[ind] = blocks_list[end_ind]
        blocks_list[end_ind] = "."
    return blocks_list[: end_ind + 1]


def get_checksum(blocks_list):
    checksum = 0
    for ind, block in enumerate(blocks_list):
        if block == ".":
            break
        checksum += ind * int(block)
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
