import sys


def marker_start(filename, block_size):
    with open(filename, 'r', encoding='utf8') as fh:
        stream = fh.readline().strip()
    for end in range(block_size, len(stream)):
        start = end - block_size
        current_chars = stream[start:end]
        if len(set(current_chars)) == block_size:
            return end


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(marker_start(input_file, 4))
    elif part == "2":
        print(marker_start(input_file, 14))
