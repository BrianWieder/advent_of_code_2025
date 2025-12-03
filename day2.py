import sys


def invalid_ids_in_range(id_range: str) -> list[int]:
    start_id_str, end_id_str = id_range.split("-")
    # If the start and end IDs have the same length and are both odd, then they cannot contain any invalid IDs
    if len(start_id_str) == len(end_id_str) and len(start_id_str) % 2 == 1:
        return []
    start_id = int(start_id_str)
    end_id = int(end_id_str)
    # Since invalid IDs are numbers with the same first and second half, we can generate them by
    # iterating over the possible values for the first half and appending it to itself
    start_half = int(
        "1"
        + "0"
        * (len(start_id_str[: len(start_id_str) // 2 + len(start_id_str) % 2]) - 1)
    )
    end_half = int("9" * len(end_id_str[len(end_id_str) // 2 :]))
    invalid_ids = []
    for i in range(start_half, end_half + 1):
        curr = f"{i}{i}"
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
    for id_range in id_ranges:
        invalid_ids.extend(invalid_ids_in_range(id_range))
    print(sum(invalid_ids))


if __name__ == "__main__":
    main()
