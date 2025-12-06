import sys
import numpy as np


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        input_file_content = f.read()

    lines = input_file_content.splitlines()
    numbers = []
    for line in lines[:-1]:
        curr_line = line.split()
        numbers.append([int(x) for x in curr_line])
    np_numbers = np.array(numbers)

    part1 = 0
    for i, operator in enumerate(lines[-1].split()):
        if operator == "*":
            part1 += np.prod(np_numbers[:, i])
        else:
            part1 += np.sum(np_numbers[:, i])
    print("Part 1:", part1)

    part2 = 0
    input_chars = [list(x) for x in lines]
    curr_nums = []
    for col in reversed(range(len(input_chars[0]))):
        curr = 0
        has_data = False
        for row in range(len(input_chars)):
            if input_chars[row][col] == "*":
                if has_data:
                    curr_nums.append(curr)
                part2 += np.prod(curr_nums)
                curr_nums = []
                has_data = False
            elif input_chars[row][col] == "+":
                if has_data:
                    curr_nums.append(curr)
                part2 += np.sum(curr_nums)
                curr_nums = []
                has_data = False
            elif "0" <= input_chars[row][col] <= "9":
                curr *= 10
                curr += int(input_chars[row][col])
                has_data = True
        if has_data:
            curr_nums.append(curr)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
