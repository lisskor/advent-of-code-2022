import sys


def read_input(filename):
    output = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            output.append([line.strip().split(" ")[0],
                           int(line.strip().split(" ")[1])])
    return output


class RopeGrid:
    def __init__(self, n_knots=2):
        self.num_knots = n_knots
        self.knot_coord = [[0, 0] for _ in range(self.num_knots)]
        self.tail_visited = [[] for _ in range(self.num_knots)]

    def head_and_tail_touching(self, head_ind, tail_ind):
        if abs(self.knot_coord[head_ind][0] - self.knot_coord[tail_ind][0]) < 2 \
                and abs(self.knot_coord[head_ind][1] - self.knot_coord[tail_ind][1]) < 2:
            return True
        else:
            return False

    def head_step(self, direction):
        if direction == 'D':
            self.knot_coord[0][0] += 1
        elif direction == 'U':
            self.knot_coord[0][0] -= 1
        elif direction == 'L':
            self.knot_coord[0][1] -= 1
        elif direction == 'R':
            self.knot_coord[0][1] += 1

    def line_command(self, direction, steps):
        for i in range(steps):
            self.head_step(direction)
            for t in range(1, self.num_knots):
                self.tail_step(t-1, t)
                self.tail_visited[t].append(tuple(self.knot_coord[t]))

    def tail_step(self, head_ind, tail_ind):
        if self.head_and_tail_touching(head_ind, tail_ind):
            return
        # If sum of coordinate differences is greater than two, it's either this situation:
        # H..
        # ..T
        # ...
        # or this situation (only in part 2):
        # H..
        # ...
        # ..T
        # Then we move the tail diagonally
        if sum(
                [abs(self.knot_coord[head_ind][0] - self.knot_coord[tail_ind][0]),
                 abs(self.knot_coord[head_ind][1] - self.knot_coord[tail_ind][1])]
        ) > 2:
            for pos in range(2):
                if self.knot_coord[head_ind][pos] > self.knot_coord[tail_ind][pos]:
                    self.knot_coord[tail_ind][pos] += 1
                elif self.knot_coord[head_ind][pos] < self.knot_coord[tail_ind][pos]:
                    self.knot_coord[tail_ind][pos] -= 1
        # If sum is 2, this situation:
        # H.T
        # Here we only need to move the tail in one direction
        else:
            for pos in range(2):
                if self.knot_coord[head_ind][pos] == self.knot_coord[tail_ind][pos]:
                    continue
                elif self.knot_coord[head_ind][pos] > self.knot_coord[tail_ind][pos]:
                    self.knot_coord[tail_ind][pos] += 1
                elif self.knot_coord[head_ind][pos] < self.knot_coord[tail_ind][pos]:
                    self.knot_coord[tail_ind][pos] -= 1


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    commands = read_input(input_file)
    if part == "1":
        grid = RopeGrid(2)
    elif part == "2":
        grid = RopeGrid(10)
    for d, n in commands:
        grid.line_command(d, n)
    print(len(set(grid.tail_visited[-1])))
