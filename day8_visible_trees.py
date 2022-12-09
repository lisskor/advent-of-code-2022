import sys
import numpy as np


def read_input(filename):
    grid = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            grid.append([int(char) for char in line.strip()])
    return np.array(grid)


class TreeGrid:
    def __init__(self, filename):
        self.trees = read_input(filename)
        self.rows, self.columns = self.trees.shape
        self.visibility = np.zeros_like(self.trees)
        for x in range(self.rows):
            for y in range(self.columns):
                self.visibility[x,y] = self.tree_is_visible(x, y)
        self.scenic = np.zeros_like(self.trees)
        for x in range(self.rows):
            for y in range(self.columns):
                self.scenic[x,y] = self.scenic_score(x, y)

    def tree_is_visible(self, x, y):
        # If on the edge, tree is always visible
        if x == 0 or y == 0:
            return 1
        # Compare height to rows in all directions
        height = self.trees[x,y]
        up, down = self.trees[:x,y], self.trees[x+1:,y]
        left, right = self.trees[x,:y], self.trees[x,y+1:]
        for side in [up, down, left, right]:
            # Tree is visible at least from one side
            if np.all(side < height):
                return 1
            else:
                continue
        # Tree is not visible if nothing returned yet
        return 0

    def scenic_score(self, x, y):
        # If on the edge, one of the directions has score 0,
        # so total score will also be 0
        if x == 0 or y == 0:
            return 0
        scenic_score = 1
        height = self.trees[x, y]
        # Reverse up and left, so we are always looking from the direction of the current tree
        up, down = self.trees[:x, y][::-1], self.trees[x + 1:, y]
        left, right = self.trees[x, :y][::-1], self.trees[x, y + 1:]
        for side in [up, down, left, right]:
            visible_trees = side < height
            if np.all(visible_trees):
                # All trees in that direction are visible
                side_score = side.shape[0]
            else:
                # Find the index of first obstructing tree and add 1
                side_score = np.where(~visible_trees)[0][0] + 1
            scenic_score *= side_score
        return scenic_score


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    trees = TreeGrid(input_file)
    if part == "1":
        print(np.sum(trees.visibility))
    elif part == "2":
        print(np.max(trees.scenic))
