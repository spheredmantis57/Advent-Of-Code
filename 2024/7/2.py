from itertools import product
import time

MULTIPLY = "*"
ADD = "+"
CONCAT = "||"
OPERATORS = [MULTIPLY, ADD, CONCAT]


def does_equal(answer, original_numbers, operator_list):
    operator_list = list(operator_list)
    numbers = original_numbers.copy()
    total = numbers[0]

    for ind, operator in enumerate(operator_list):
        if operator == MULTIPLY:
            total *= numbers[ind + 1]
        elif operator == ADD:
            total += numbers[ind + 1]
        else:  # Concat
            total = int(f"{total}{numbers[ind + 1]}")
    return total == answer


def can_produce_test_value(answer, numbers):
    operator_slots = len(numbers) - 1
    possible_operators_list = list(product(OPERATORS, repeat=operator_slots))
    for operator_list in possible_operators_list:
        if does_equal(answer, numbers, operator_list):
            return True


def main():
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    total = 0
    for line in lines:
        line = line.strip().split(":")
        answer = int(line[0])
        num_list = [int(num) for num in line[1][1:].split(" ")]
        if can_produce_test_value(answer, num_list):
            total += answer
    print(f"{total = }")


if __name__ == "__main__":
    print("Start Solve")
    start = time.time()
    main()
    end = time.time()
    print("Done Solve")
    print(f"Took {end - start:.4f} seconds")
