import sys

def count_zeros(input_content: str) -> tuple[int, int]:
    pos = 50
    exact_count = 0
    all_zeros = 0
    for op in input_content.split():
        rotation_amount = int(op[1:])
        if op.startswith('L'):
            rotation_amount *= -1
        elif op.startswith('R'):
            pass
        else:
            raise ValueError('Unexpected direction', op)
        # If we started at 0 and rotating left, we don't want to count the first rotation as crossing 0
        if pos == 0 and op.startswith('L'):
            all_zeros -= 1
        pos += rotation_amount
        # Count the number of times we pass 0 when turning left
        while pos < 0:
            all_zeros += 1
            pos += 100
        # Count the number of times we pass 0 when turning right
        while pos > 99:
            all_zeros += 1
            pos -= 100
        # If we end at 0 when turning right, that means we hit the above pos > 99 case, and we want to remove one increment, since we increment below
        if pos == 0 and op.startswith('R'):
            all_zeros -= 1
        if pos == 0:
            exact_count += 1
            all_zeros += 1
    return (exact_count, all_zeros)
    

def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected a single argument for the input file")
    input_file_name = sys.argv[1]
    with open(input_file_name, 'r') as f:
        input_file_content = f.read()
    print(count_zeros(input_file_content))

if __name__ == "__main__":
    main()