import sys
from string import ascii_lowercase, ascii_uppercase


def priorities_sum(filename, priorities):
    total = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            contents = line.strip()
            comp1, comp2 = contents[:len(contents)//2], contents[len(contents)//2:]
            error = list(set(comp1).intersection(set(comp2)))[0]
            total += priorities[error]
    return total


def badges(filename, priorities):
    total = 0
    num_in_group = 0
    current_group = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            current_group.append(line.strip())
            num_in_group += 1
            if num_in_group == 3:
                badge = list(set(current_group[0]).intersection(set(current_group[1])).intersection(current_group[2]))[0]
                total += priorities[badge]
                num_in_group = 0
                current_group = []
    return total


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    char_priorities = {}
    for i, char in enumerate(ascii_lowercase):
        char_priorities[char] = i + 1
    for i, char in enumerate(ascii_uppercase):
        char_priorities[char] = i + 27
    if part == "1":
        print(priorities_sum(input_file, char_priorities))
    elif part == "2":
        print(badges(input_file, char_priorities))
