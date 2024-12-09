import time
from pathlib import Path


class Antenna:
    def __init__(self, freq, x=0, y=0):
        self.x = x
        self.y = y
        self.freq = freq

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"antenna {self.freq}: [{self.x}, {self.y}]"

    def calculate_antinodes(self, other, x_len, y_len):
        # todo take out
        # if self.freq == "T":
        #     raise ValueError("0")

        if self.freq != other.freq:
            raise ValueError("Freqs must match to get an antinode")
        if self == other:
            raise ValueError("Cannot get an antinode with yourself")

        x_delta_signed = self.x - other.x
        x_delta = abs(x_delta_signed)
        y_delta_signed = self.y - other.y
        y_delta = abs(y_delta_signed)
        x_delta_original = x_delta
        y_delta_original = y_delta

        antinodes_list = []

        max_x = 0
        max_y = 0
        try:
            max_x = int(x_len / x_delta) + 1
        except ZeroDivisionError:
            pass
        try:
            max_y = int(y_len / y_delta) + 1
        except ZeroDivisionError:
            pass
        times = max(max_x, max_y)

        for _ in range(times):
            antinode_1 = Antenna(self.freq)
            antinode_2 = Antenna(self.freq)

            # get our right and left for the antinodes
            if x_delta_signed <= 0:
                # left most or middle
                antinode_1.x = self.x - x_delta
                antinode_2.x = other.x + x_delta
            else:
                # right most
                antinode_1.x = self.x + x_delta
                antinode_2.x = other.x - x_delta

            # get our top and bottom for the antinodes
            if y_delta_signed >= 0:
                # bottom most or middle
                antinode_1.y = self.y + y_delta
                antinode_2.y = other.y - y_delta
            else:
                # upper most
                antinode_1.y = self.y - y_delta
                antinode_2.y = other.y + y_delta

            for antinode in [antinode_1, antinode_2]:
                if 0 <= antinode.x < x_len and 0 <= antinode.y < y_len:
                    antinodes_list.append(antinode)

            x_delta += x_delta_original
            y_delta += y_delta_original

        return antinodes_list


def count_antinodes(lines):
    antinodes = set()
    antennas = set()

    # Find all antennas
    for y_ind, line in enumerate(lines):
        for x_ind, point in enumerate(line):
            if point != ".":
                antenna = Antenna(point, x_ind, y_ind)
                antennas.add(antenna)
                antinodes.add(antenna)

    # Get all antinodes
    x_len = len(lines[0])
    y_len = len(lines)
    other_antennas = antennas.copy()
    for antenna in antennas:
        for other_antenna in other_antennas:
            try:
                new_antinodes = antenna.calculate_antinodes(other_antenna, x_len, y_len)
                for antinode in new_antinodes:
                    if 0 <= antinode.x < x_len and 0 <= antinode.y < y_len:
                        antinodes.add(antinode)
            except ValueError:
                pass
        # Don't double count for no reason
        other_antennas.discard(antenna)

    return len(antinodes)


def main():
    file_path = Path("input.txt")
    lines = file_path.read_text().splitlines()
    print(f"total {count_antinodes(lines)}")


if __name__ == "__main__":
    print("Start Solve")
    start = time.time()
    main()
    end = time.time()
    print("Done Solve")
    print(f"Took {end - start:.4f} seconds")
