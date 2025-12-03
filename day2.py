import sys


def invalid_ids_with_n_repetitions(id_range: str, n: int) -> list[int]:
    start_id_str, end_id_str = id_range.split("-")
    start_id = int(start_id_str)
    end_id = int(end_id_str)
    start_id_len = len(start_id_str)
    end_id_len = len(end_id_str)
    invalid_ids = []

    for i in range(start_id_len, end_id_len + 1):
        if i % n != 0:
            continue
        start_half = "1" + "0" * (i // n - 1)
        end_half = "9" * (i // n)
        for j in range(int(start_half), int(end_half) + 1):
            curr = f"{j}" * n
            if int(curr) < start_id:
                continue
            # Once we go past the end ID, we can break since we will only generate larger IDs
            if int(curr) > end_id:
                break
            invalid_ids.append(int(curr))
    return invalid_ids


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        input_file_content = f.read()
    id_ranges = input_file_content.split(",")
    invalid_ids = []
    max_length = 0
    for id_range in id_ranges:
        max_length = max(max_length, len(id_range.split("-")[1]))
        invalid_ids.extend(invalid_ids_with_n_repetitions(id_range, 2))
    print("Part 1: ", sum(invalid_ids))
    part_2_invalid_ids = set()
    for id_range in id_ranges:
        for i in range(2, len(id_range.split("-")[1]) + 1):
            part_2_invalid_ids.update(invalid_ids_with_n_repetitions(id_range, i))
    print("Part 2: ", sum(part_2_invalid_ids))


if __name__ == "__main__":
    main()
