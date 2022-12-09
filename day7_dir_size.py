import sys


def total_sizes(filename):
    tree = DirTree()
    current_path = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            clean_line = line.strip()
            if clean_line == "$ cd /":
                current_path.append("/")
                current_dir = "/"
                parent = None
            elif clean_line == "$ cd ..":
                # When going up, save what has been accumulated from previous ls
                # If the directory already exists in the tree, it will be skipped
                prev_directory = Directory(current_dir, parent, current_path, subdirs, files)
                tree.add_dir(prev_directory)
                # Keep track of where we end up after going one level up
                current_path.pop()
                current_dir = current_path[-1]
            elif clean_line.startswith('$ cd'):
                # When going to a subdirectory, save what has been accumulated from previous ls
                prev_directory = Directory(current_dir, parent, current_path, subdirs, files)
                tree.add_dir(prev_directory)
                parent = ":".join(current_path)
                current_dir = clean_line.split(' ')[2]
                # Keep track of the path
                current_path.append(current_dir)
            elif clean_line == "$ ls":
                # When doing ls in a new directory, reset the subdirs and files lists
                subdirs = []
                files = []
            elif clean_line.startswith('dir'):
                # Add dir to list of subdirectories
                subdirs.append(clean_line.split(' ')[1])
            else:
                # Add file
                files.append((clean_line.split(' ')[1],
                              int(clean_line.split(' ')[0])))
        # Process current state after the last line has been read
        prev_directory = Directory(current_dir, parent, current_path, subdirs, files)
        tree.add_dir(prev_directory)
    return tree


class DirTree:
    def __init__(self):
        self.tree = dict()
        self.properties = dict()

    def __repr__(self):
        return str(self.tree)

    def add_dir(self, directory):
        # Skip adding if directory is already present
        if directory.full_path in self.tree:
            return
        # Add to parent-child tree
        self.tree[directory.full_path] = []
        # Add to parent's child list
        if directory.name != '/' and directory.name not in self.tree[directory.parent]:
            self.tree[directory.parent].append(directory.name)
        # Save properties in a second dict (e.g. files)
        self.properties[directory.full_path] = directory
        # Add subdirectories to this directory's child list
        for child in directory.subdirs:
            if child not in self.tree[directory.full_path]:
                self.tree[directory.full_path].append(child)
        # Increase parent's size recursively
        self.increase_parent_size(directory.full_path, directory.size)

    def increase_parent_size(self, directory, dir_size):
        if self.properties[directory].parent is None:
            pass
        else:
            self.properties[self.properties[directory].parent].size += dir_size
            self.increase_parent_size(self.properties[directory].parent, dir_size)

    def count_total_under_x(self, x=100000):
        total = 0
        for d in self.tree:
            if self.properties[d].size <= x:
                total += self.properties[d].size
        return total

    def directory_to_delete(self):
        filesystem_size = 70000000
        needed_space = 30000000
        unused_space = filesystem_size - self.properties['/'].size
        space_to_free = needed_space - unused_space
        smallest_size_to_remove = self.properties['/'].size
        for d in self.tree:
            d_size = self.properties[d].size
            if space_to_free <= d_size < smallest_size_to_remove:
                smallest_size_to_remove = d_size
        return smallest_size_to_remove


class Directory:
    def __init__(self, name, parent, full_path, subdirs, files):
        self.name = name
        self.parent = parent
        self.full_path = ":".join(full_path)
        self.subdirs = subdirs
        self.files = files
        self.size = sum([f[1] for f in self.files])

    def __repr__(self):
        return f"path {self.full_path} | dirs {self.subdirs} | files {self.files} | size {self.size}"


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    structure = total_sizes(input_file)
    # print(structure)
    # for k in structure.properties:
    #     print(f"{k} : {structure.properties[k]}")
    if part == "1":
        print(structure.count_total_under_x())
    elif part == "2":
        print(structure.directory_to_delete())
