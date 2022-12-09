import sys


def read_input(filename):
    initial_state, instructions = [], []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            if line.strip().startswith('[') or line.strip().startswith('1'):
                initial_state.append(line)
            elif line.strip().startswith('move'):
                instructions.append([int(word) for (i, word)
                                     in enumerate(line.strip().split(" "))
                                     if i % 2 == 1])
            else:
                pass
    return initial_state, instructions


def top_crates(filename, move_multiple=False):
    init_state, instructions = read_input(filename)
    crates = CrateStacks(init_state)
    for num, from_stack, to_stack in instructions:
        if move_multiple:
            crates.move_multiple_alt(num, from_stack-1, to_stack-1)
        else:
            crates.move(num, from_stack-1, to_stack-1)
    return ''.join([stack[-1] for stack in crates.stacks])


class CrateStacks:
    def __init__(self, initial_state: list[str]):
        self.num_stacks, self.stacks = self.process_initial_state(initial_state)

    def __repr__(self):
        stack_string = "\n".join([str(stack) for stack in self.stacks])
        return f"Stacks: {self.num_stacks}\n{stack_string}"

    def process_initial_state(self, initial_state: list[str]):
        num_stacks = int(initial_state[-1].strip()[-1])
        stacks = [[] for s in range(num_stacks)]
        for initial_line in initial_state[::-1][1:]:
            for i in range(num_stacks):
                if initial_line[4*i + 1] != ' ':
                    stacks[i].append(initial_line[4*i + 1])
        return num_stacks, stacks

    def move(self, crates_num: int, move_from: int, move_to: int):
        for i in range(crates_num):
            self.stacks[move_to].append(self.stacks[move_from].pop())

    def move_multiple(self, crates_num: int, move_from: int, move_to: int):
        # Create an extra stack and use function for moving a single crate
        self.stacks.append([])
        for i in range(crates_num):
            self.move(1, move_from, -1)
        for i in range(crates_num):
            self.move(1, -1, move_to)
        self.stacks = self.stacks[:-1]

    def move_multiple_alt(self, crates_num: int, move_from: int, move_to: int):
        # Alternatively, use slicing to move multiple stacks at once
        self.stacks[move_to].extend(self.stacks[move_from][-crates_num:])
        self.stacks[move_from] = self.stacks[move_from][:-crates_num]


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(top_crates(input_file, False))
    elif part == "2":
        print(top_crates(input_file, True))
