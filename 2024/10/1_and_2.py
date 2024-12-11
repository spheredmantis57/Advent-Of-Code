from pathlib import Path
import time

MAP = None

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if -1 in [x,y]:
            raise IndexError("Off map")
        self.elevation = int(MAP[y][x])

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    @staticmethod
    def fill_accessible_peaks(curr_location, list_of_accessible_peaks):
        if curr_location.elevation == 9:
            list_of_accessible_peaks.append(curr_location)
            return
        left = (curr_location.x - 1, curr_location.y)
        right = (curr_location.x + 1, curr_location.y)
        up = (curr_location.x, curr_location.y - 1)
        down = (curr_location.x, curr_location.y + 1)
        for neighbor in [left, right, up, down]:
            try:
                neighbor = Location(neighbor[0], neighbor[1])
            except IndexError:
                continue
            if neighbor.elevation - 1 == curr_location.elevation:
                Location.fill_accessible_peaks(neighbor, list_of_accessible_peaks)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class TrailHead(Location):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.accessible_peaks = []

    def add_accessible_peaks(self):
        self.fill_accessible_peaks(self, self.accessible_peaks)


def get_locations():
    peaks = []  # Dont need peaks right now but its easy to just save incase
    heads = []
    for ind_y, line in enumerate(MAP):
        for ind_x, square in enumerate(line):
            if square == "0":
                heads.append(TrailHead(ind_x, ind_y))
            elif square == "9":
                peaks.append(Location(ind_x, ind_y))
    return peaks, heads


def score_and_rate_individual_head(head):
    head.add_accessible_peaks()
    score = len(head.accessible_peaks)
    rating = len(set(head.accessible_peaks))
    return score, rating


def score_and_rate_trailheads(heads):
    total_score = 0
    total_rating = 0
    for head in heads:
        score, rating = score_and_rate_individual_head(head)
        total_rating += rating
        total_score += score
    return total_score, total_rating


def main():
    global MAP
    file_path = Path("input.txt")
    MAP = file_path.read_text().splitlines()
    _, heads = get_locations()
    total_score, total_rating = score_and_rate_trailheads(heads)
    print(f"{total_score = }\n{total_rating}")


if __name__ == "__main__":
    print("Start Solve")
    start = time.time()
    main()
    end = time.time()
    print("Done Solve")
    print(f"Took {end - start:.4f} seconds")