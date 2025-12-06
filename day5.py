import sys
import enum


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __lt__(self, other: "Range") -> bool:
        if self.end == other.end:
            return self.start < other.start
        return self.end < other.end

    def __repr__(self) -> str:
        return f"Range({self.start}, {self.end})"

    def should_merge(self, other: "Range") -> bool:
        return self.end >= other.start

    def merge(self, other: "Range") -> "Range":
        return Range(min(self.start, other.start), max(self.end, other.end))


def is_with_ranges(line: int, ranges: list[Range]) -> bool:
    for range in ranges:
        if range.start <= line <= range.end:
            return True
    return False


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        input_file_content = f.read()

    lines = input_file_content.splitlines()
    fresh_ranges = []
    empty_line_index = 0
    for i, line in enumerate(lines):
        if line == "":
            empty_line_index = i
            break
        start, end = line.split("-")
        fresh_ranges.append(Range(int(start), int(end)))

    fresh_ranges.sort()

    # Merge overlapping ranges
    i = 0
    while i < len(fresh_ranges):
        if i + 1 < len(fresh_ranges) and fresh_ranges[i].should_merge(
            fresh_ranges[i + 1]
        ):
            fresh_ranges[i] = fresh_ranges[i].merge(fresh_ranges[i + 1])
            fresh_ranges.pop(i + 1)
        else:
            i += 1

    part1 = 0
    for i in lines[empty_line_index + 1 :]:
        if is_with_ranges(int(i), fresh_ranges):
            part1 += 1

    part2 = 0
    for i in fresh_ranges:
        part2 += (i.end - i.start) + 1

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
