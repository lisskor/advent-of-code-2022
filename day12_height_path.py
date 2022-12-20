import sys
import numpy as np
from string import ascii_lowercase


def read_input(filename):
    heights_dict = {char: n for n, char in enumerate(ascii_lowercase)}
    heights_dict['S'] = 0
    heights_dict['E'] = 25
    output = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line_num, line in enumerate(fh):
            line_heights = []
            for char_num, char in enumerate(line.strip()):
                line_heights.append(heights_dict[char])
                if char == 'S':
                    start_pos = (line_num, char_num)
                if char == 'E':
                    end_pos = (line_num, char_num)
            output.append(line_heights)
    return np.array(output), start_pos, end_pos


def reconstruct_path(came_from, current):
    total_path = []
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path



class HeightGraph:
    def __init__(self, heights, start, end):
        self.heightmap = heights
        self.heightmap = np.pad(self.heightmap, pad_width=1, mode='constant', constant_values=30)
        self.start = (start[0] + 1, start[1] + 1)
        self.end = (end[0] + 1, end[1] + 1)
        self.graph = {}
        self.build_graph()

    def build_graph(self):
        for row in range(1, self.heightmap.shape[0]-1):
            for col in range(1, self.heightmap.shape[1]-1):
                self.graph[(row, col)] = []
                for neighbor in [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]:
                    if self.is_reachable((row, col), neighbor):
                        self.graph[(row, col)].append(neighbor)

    def is_reachable(self, source, destination):
        if abs(source[0] - destination[0]) + abs(source[1] - destination[1]) == 1:
            if self.heightmap[destination] - self.heightmap[source] < 2:
                return True
        return False

    def a_star(self, start):
        # Based on pseudocode from Wikipedia:
        # https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
        open_set = [start]
        came_from = {}
        # g_score is the length of shortest currently known path to each point
        g_score = {vertex: float('inf') for vertex in self.graph}
        g_score[start] = 0
        # f_score is the current best guess of how cheap a path through
        # a particular node can be
        f_score = {vertex: float('inf') for vertex in self.graph}
        f_score[start] = sum([abs(start[x] - self.end[x]) for x in range(1)])

        while open_set:
            current = min(open_set, key=lambda x: f_score[x])
            if current == self.end:
                return reconstruct_path(came_from, current)
            open_set.remove(current)
            for neighbor in self.graph[current]:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + sum([abs(neighbor[x] - self.end[x]) for x in range(1)])
                    if neighbor not in open_set:
                        open_set.append(neighbor)
        return None

    def multiple_starting_points(self):
        shortest_path_from_a_to_end = float('inf')
        for node in self.graph:
            if self.heightmap[node] == 0:
                shortest_path_from_node = self.a_star(node)
                if shortest_path_from_node is None:
                    continue
                elif len(shortest_path_from_node) < shortest_path_from_a_to_end:
                    shortest_path_from_a_to_end = len(shortest_path_from_node)
        return shortest_path_from_a_to_end


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    heightmap = HeightGraph(*read_input(input_file))
    if part == "1":
        print(f"Length of shortest path from start to end: {len(heightmap.a_star(heightmap.start))}")
    elif part == "2":
        print(f"Length of shortest path from any point with elevation a to end: {heightmap.multiple_starting_points()}")
