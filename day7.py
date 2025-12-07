import sys
import enum


class Tile(enum.Enum):
    EMPTY = enum.auto()
    START = enum.auto()
    SPLITTER = enum.auto()
    LASER = enum.auto()

    def __str__(self):
        return {
            Tile.EMPTY: ".",
            Tile.START: "S",
            Tile.SPLITTER: "^",
            Tile.LASER: "|",
        }[self]


def parse_input(input_file_content: str) -> tuple[list[list[Tile]], tuple[int, int]]:
    board = []
    for row, line in enumerate(input_file_content.splitlines()):
        curr_row = []
        for col, x in enumerate(line):
            if x == "S":
                start = (row, col)
            match x:
                case ".":
                    curr_row.append(Tile.EMPTY)
                case "S":
                    curr_row.append(Tile.START)
                case "^":
                    curr_row.append(Tile.SPLITTER)
                case _:
                    raise ValueError(f"Unknown tile: {x}")
        board.append(curr_row)
    return board, start


# Once trace the number of timelines spawned below a splitter once, cache the results for other splitters to avoid redundant work
_part_2_cache = {}


def trace_laster(board: list[list[Tile]], start: tuple[int, int]) -> tuple[int, int]:
    x, y = start
    if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
        # Not a split, but is a timeline end
        return 0, 1
    if board[x][y] == Tile.EMPTY:
        board[x][y] = Tile.LASER
        # continues downward without any new timelines
        unique, timelines = trace_laster(board, (x + 1, y))
        _part_2_cache[start] = timelines
        return unique, timelines
    if board[x][y] == Tile.SPLITTER:
        left_unique_lasers, left_timelines = trace_laster(board, (x, y + 1))
        right_unique_lasers, right_timelines = trace_laster(board, (x, y - 1))
        _part_2_cache[start] = left_timelines + right_timelines
        return (
            1 + left_unique_lasers + right_unique_lasers,
            left_timelines + right_timelines,
        )
    # If we reach a laser, this is a duplicate laser, and we have already cached the number of timelines spawned below the splitter
    if board[x][y] == Tile.LASER:
        return 0, _part_2_cache[start]
    return 0, 0


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        input_file_content = f.read()
    board, start = parse_input(input_file_content)
    start_x, start_y = start
    part1, part2 = trace_laster(board, (start_x + 1, start_y))
    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
