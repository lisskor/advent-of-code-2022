import sys


def total_score(filename):
    total = 0
    own_play_scores = {'X': 1, 'Y': 2, 'Z': 3}
    outcome_scores = {'AX': 3, 'BY': 3, 'CZ': 3,
                      'AZ': 0, 'BX': 0, 'CY': 0,
                      'AY': 6, 'BZ': 6, 'CX': 6}
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            play = ''.join(line.strip().split(" "))
            total += own_play_scores[play[1]]
            total += outcome_scores[play]
    return total


def total_score_p2(filename):
    total = 0
    own_play_scores = {'A': 1, 'B': 2, 'C': 3}
    outcome_scores = {'X': 0, 'Y': 3, 'Z': 6}
    moves = {'AY': 'A', 'BY': 'B', 'CY': 'C',
             'AX': 'C', 'BX': 'A', 'CX': 'B',
             'AZ': 'B', 'BZ': 'C', 'CZ': 'A'}
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            instructions = ''.join(line.strip().split(" "))
            play = moves[instructions]
            total += own_play_scores[play]
            total += outcome_scores[instructions[1]]
    return total


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(total_score(input_file))
    elif part == "2":
        print(total_score_p2(input_file))
