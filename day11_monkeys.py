import sys


def read_input(filename):
    output = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            clean_line = line.strip()
            if clean_line.startswith("Monkey"):
                monkey_dict = {'n': int(clean_line.split(" ")[-1][:-1])}
            elif clean_line.startswith("Starting"):
                monkey_dict['items'] = [int(i.strip()) for i in clean_line.split(":")[-1].split(',')]
            elif clean_line.startswith("Operation"):
                monkey_dict['operation_string'] = clean_line.split("=")[1].strip()
            elif clean_line.startswith("Test"):
                monkey_dict['divide_by'] = int(clean_line.split(" ")[-1])
            elif clean_line.startswith("If true"):
                monkey_dict['throw_to_if_true'] = int(clean_line.split(" ")[-1])
            elif clean_line.startswith("If false"):
                monkey_dict['throw_to_if_false'] = int(clean_line.split(" ")[-1])
                output.append(monkey_dict)
    return output


class Monkeys:
    def __init__(self, monkeys_list, task_part):
        self.part = task_part
        self.monkeys = []
        for m_dict in monkeys_list:
            self.monkeys.append(Monkey(m_dict))

    def __repr__(self):
        return "\n".join([str(mnk) for mnk in self.monkeys])

    def turn(self):
        for monkey in self.monkeys:
            for item in monkey.items:
                old = item.worry_level
                if self.part == 2:
                    # Take remainder after dividing by product of all monkeys' test denominators
                    item.worry_level = eval(monkey.operation_string) % (eval("*".join([str(m.divide_by)
                                                                                       for m in self.monkeys])))
                elif self.part == 1:
                    item.worry_level = eval(monkey.operation_string)
                    item.worry_level = int(item.worry_level / 3)
                if item.worry_level % monkey.divide_by == 0:
                    self.monkeys[monkey.throw_to_if_true].items.append(item)
                else:
                    self.monkeys[monkey.throw_to_if_false].items.append(item)
                monkey.total_inspected += 1
            monkey.items = []


class Item:
    def __init__(self, worry_level):
        self.worry_level = worry_level


class Monkey:
    def __init__(self, monkey_dict):
        for key in monkey_dict:
            setattr(self, key, monkey_dict[key])
        self.items = [Item(item) for item in monkey_dict['items']]
        self.total_inspected = 0

    def __repr__(self):
        return f"Monkey {self.n}: {self.total_inspected}"


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        monkeys = Monkeys(read_input(input_file), 1)
        turns = 20
    elif part == "2":
        monkeys = Monkeys(read_input(input_file), 2)
        turns = 10000
    for i in range(turns):
        monkeys.turn()
    print(monkeys)
    two_most_active = sorted([m.total_inspected for m in monkeys.monkeys], reverse=True)[:2]
    print(f"Monkey business: {two_most_active[0] * two_most_active[1]}")
