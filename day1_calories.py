import sys


def most_calories(filename):
    max_calories = 0
    current_calories = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            if not line.strip():
                if max_calories < current_calories:
                    max_calories = current_calories
                current_calories = 0
            else:
                current_calories += int(line.strip())
    if max_calories < current_calories:
        max_calories = current_calories
    return max_calories


def top_3_most_calories(filename):
    elves = []
    current_calories = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            if not line.strip():
                elves.append(current_calories)
                current_calories = 0
            else:
                current_calories += int(line.strip())
    elves.append(current_calories)
    return sum(sorted(elves, reverse=True)[:3])


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(most_calories(input_file))
    elif part == "2":
        print(top_3_most_calories(input_file))
