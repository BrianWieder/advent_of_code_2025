import sys


def max_joltage_from_bank(bank: list[int], n=2) -> int:
    val = 0
    start_index = 0
    for i in reversed(range(n)):
        # If we are at the last iteration, we want to include all the way to the end
        if i == 0:
            i = None
        else:
            # Otherwise, we want to index from the end
            i *= -1
        max_val = max(bank[start_index:i])
        # When we find the max value, we want to move the start index to the right of it, so we can find the next max value
        start_index = bank[start_index:i].index(max_val) + start_index + 1
        val *= 10
        val += max_val
    return val


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        input_file_content = f.read()

    swap2_joltages = []
    swap12_joltages = []
    for line in input_file_content.splitlines():
        bank = [int(joltage) for joltage in line]
        swap2_joltages.append(max_joltage_from_bank(bank))
        swap12_joltages.append(max_joltage_from_bank(bank, 12))
    print("Part 1: ", sum(swap2_joltages))
    print("Part 2: ", sum(swap12_joltages))


if __name__ == "__main__":
    main()
