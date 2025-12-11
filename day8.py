from collections import defaultdict
import heapq
import math
import sys
import dataclasses
import functools


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int
    z: int


@dataclasses.dataclass(frozen=True)
class JunctionBox:
    position: Position

    def get_distance(self, other: "JunctionBox") -> int:
        return math.sqrt(
            (self.position.x - other.position.x) ** 2
            + (self.position.y - other.position.y) ** 2
            + (self.position.z - other.position.z) ** 2
        )


def parse_input(input_file_content: str) -> list[JunctionBox]:
    lines = input_file_content.splitlines()
    junction_boxes = []
    for line in lines:
        x, y, z = map(int, line.split(","))
        junction_boxes.append(JunctionBox(Position(x, y, z)))
    return junction_boxes


def main():
    if len(sys.argv) != 3:
        raise ValueError("Expected two arguments for the input file")

    input_file_name = sys.argv[1]
    num_connections_to_make = int(sys.argv[2])
    with open(input_file_name, "r") as f:
        input_file_content = f.read()
    junction_boxes = parse_input(input_file_content)
    distances = {}
    distances_heap = []

    # Calculate all distances between boxes and push them into a heap
    for box in junction_boxes:
        for other_box in junction_boxes:
            curr_set = frozenset({box, other_box})
            if box != other_box and curr_set not in distances:
                distances[curr_set] = box.get_distance(other_box)
                heapq.heappush(distances_heap, (distances[curr_set], curr_set))

    circuits = {}
    inverse_circuits = defaultdict(set)
    num_circuits = 0
    last_connected = (None, None)
    part1 = 0

    # Use the heap to connect the closest boxes until we have exhausted the connections
    while distances_heap:
        distance, boxes = heapq.heappop(distances_heap)
        boxes = list(boxes)

        # If we did all the iterations for part1, calculate it, and continue
        # for part2
        if num_connections_to_make == 0:
            circuit_sizes = []
            for circuit in inverse_circuits.values():
                if not circuit:
                    continue
                circuit_sizes.append(len(list(circuit)))
            circuit_sizes.sort()
            part1 = functools.reduce(lambda x, y: x * y, circuit_sizes[-3:])

        num_connections_to_make -= 1
        if boxes[0] not in circuits and boxes[1] not in circuits:
            circuits[boxes[0]] = num_circuits
            circuits[boxes[1]] = num_circuits
            inverse_circuits[num_circuits] = {boxes[0], boxes[1]}
            num_circuits += 1
        elif boxes[0] in circuits and boxes[1] not in circuits:
            circuits[boxes[1]] = circuits[boxes[0]]
            inverse_circuits[circuits[boxes[0]]].add(boxes[1])
        elif boxes[1] in circuits and boxes[0] not in circuits:
            circuits[boxes[0]] = circuits[boxes[1]]
            inverse_circuits[circuits[boxes[1]]].add(boxes[0])
        elif boxes[0] in circuits and boxes[1] in circuits:
            new_circuit = circuits[boxes[0]]
            old_circuit = circuits[boxes[1]]
            if new_circuit == old_circuit:
                continue
            for box in inverse_circuits[old_circuit]:
                circuits[box] = new_circuit
            inverse_circuits[new_circuit].update(inverse_circuits[old_circuit])
            inverse_circuits.pop(old_circuit)
        else:
            raise ValueError("Unknown case")
        # Keep track of the last connection for part2
        last_connected = (boxes[0], boxes[1])
    print("Part 1:", part1)
    print("Part 2:", last_connected[0].position.x * last_connected[1].position.x)


if __name__ == "__main__":
    main()
