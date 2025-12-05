import sys
import enum


class BoardSquare(enum.Enum):
    EMPTY = 0
    TP = 1

    def __str__(self):
        if self == BoardSquare.EMPTY:
            return "."
        elif self == BoardSquare.TP:
            return "@"
        else:
            raise ValueError("Invalid board square: " + str(self))


def print_board(board: list[list[BoardSquare]]):
    for row in board:
        print("".join([str(x) for x in row]))


def count_surrounding(board: list[list[BoardSquare]], x: int, y: int) -> int:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x + i < 0 or x + i >= len(board) or y + j < 0 or y + j >= len(board[0]):
                continue
            if board[x + i][y + j] == BoardSquare.TP:
                count += 1
    return count


def create_board(board_str: str) -> list[list[BoardSquare]]:
    board = []
    for line in board_str.splitlines():
        curr = []
        for c in line:
            if c == ".":
                curr.append(BoardSquare.EMPTY)
            elif c == "@":
                curr.append(BoardSquare.TP)
            else:
                raise ValueError("Invalid board character: " + c)
        board.append(curr)
    return board


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, "r") as f:
        input_file_content = f.read()
    board = create_board(input_file_content)
    part1 = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == BoardSquare.TP:
                if count_surrounding(board, i, j) < 4:
                    part1 += 1

    removed = True
    part2 = 0
    while removed:
        removed = False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == BoardSquare.TP:
                    if count_surrounding(board, i, j) < 4:
                        removed = True
                        board[i][j] = BoardSquare.EMPTY
                        part2 += 1

    print("Part 1: " + str(part1))
    print("Part 2: " + str(part2))


if __name__ == "__main__":
    main()
