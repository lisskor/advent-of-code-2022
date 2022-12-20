import sys


def read_input(filename):
    output = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            output.append(line.strip().split(" "))
    return output


class Circuit:
    def __init__(self):
        self.cycle = 0
        self.x = 1
        self.signal_strength_sum = 0
        self.screen = [['.' for _ in range(40)] for _ in range(6)]

    def __repr__(self):
        return "\n".join([' '.join(row) for row in self.screen])

    def do_instructions(self, instructions):
        for instruction in instructions:
            self.step()
            action = instruction[0]
            if action == 'addx':
                increment = int(instruction[1])
                self.step(increment)

    def step(self, increment=0):
        self.draw()
        self.cycle += 1
        self.x += increment
        if self.cycle == 19 or (self.cycle - 19) % 40 == 0:
            self.signal_strength_sum += self.x * (self.cycle + 1)

    def draw(self):
        pixel_row = self.cycle // 40
        pixel_col = self.cycle % 40
        # Check if sprite is visible (width 3)
        if abs(pixel_col - self.x) < 2:
            self.screen[pixel_row][pixel_col] = '#'


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    commands = read_input(input_file)
    circuit = Circuit()
    circuit.do_instructions(commands)
    print(f"Sum: {circuit.signal_strength_sum}")
    print(circuit)
