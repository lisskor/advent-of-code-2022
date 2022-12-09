import sys


def a_contains_b(a, b):
    if a[0] <= b[0] and a[-1] >= b[-1]:
        return True
    else:
        return False


def overlap(a, b):
    if a[-1] >= b[0] and a[0] <= b[-1]:
        return True
    if b[-1] >= a[0] and b[0] <= a[-1]:
        return True
    return False


def pair_overlaps(filename):
    total = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            sections = [[int(num) for num in assignment.split("-")] for assignment in line.strip().split(",")]
            if a_contains_b(sections[0], sections[1]) or a_contains_b(sections[1], sections[0]):
                total += 1
    return total


def all_pair_overlaps(filename):
    total = 0
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            sections = [[int(num) for num in assignment.split("-")] for assignment in line.strip().split(",")]
            if a_contains_b(sections[0], sections[1]) or a_contains_b(sections[1], sections[0]) or overlap(sections[0], sections[1]):
                total += 1
    return total


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(pair_overlaps(input_file))
    elif part == "2":
        print(all_pair_overlaps(input_file))
