import sys
import re
from collections import namedtuple
from ipdb import launch_ipdb_on_exception


def main(commands):
    """
    --- Day 7: No Space Left On Device ---

    You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
    Occasionally, you can even hear much louder sounds in the distance; how big do the animals get
    out here, anyway?

    The device the Elves gave you has problems with more than just its communication system. You try
    to run a system update:

    $ system-update --please --pretty-please-with-sugar-on-top Error: No space left on device

    Perhaps you can delete some files to make space for the update?

    You browse around the filesystem to assess the situation and save the resulting terminal output
    (your puzzle input). For example:

    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k

    The filesystem consists of a tree of files (plain data) and directories (which can contain other
    directories or files). The outermost directory is called /. You can navigate around the
    filesystem, moving into or out of directories and listing the contents of the directory you're
    currently in.

    Within the terminal output, lines that begin with $ are commands you executed, very much like
    some modern computers:

      - cd means change directory. This changes which directory is the current directory, but the
        specific result depends on the argument:
          - cd x moves in one level: it looks in the current directory for the directory named x and
            makes it the current directory.
          - cd .. moves out one level: it finds the directory that contains the current directory,
            then makes that directory the current directory.
          - cd / switches the current directory to the outermost directory, /.
      - ls means list. It prints out all of the files and directories immediately contained by the
        current directory:
          - 123 abc means that the current directory contains a file named abc with size 123.
          - dir xyz means that the current directory contains a directory named xyz.

    Given the commands and output in the example above, you can determine that the filesystem looks
    visually like this:

    - / (dir)
      - a (dir)
        - e (dir)
          - i (file, size=584)
        - f (file, size=29116)
        - g (file, size=2557)
        - h.lst (file, size=62596)
      - b.txt (file, size=14848514)
      - c.dat (file, size=8504156)
      - d (dir)
        - j (file, size=4060174)
        - d.log (file, size=8033020)
        - d.ext (file, size=5626152)
        - k (file, size=7214296)

    Here, there are four directories: / (the outermost directory), a and d (which are in /), and e
    (which is in a). These directories also contain files of various sizes.

    Since the disk is full, your first step should probably be to find directories that are good
    candidates for deletion. To do this, you need to determine the total size of each directory.
    The total size of a directory is the sum of the sizes of the files it contains, directly or
    indirectly. (Directories themselves do not count as having any intrinsic size.)

    The total sizes of the directories above can be found as follows:

      - The total size of directory e is 584 because it contains a single file i of size 584 and no
        other directories.
      - The directory a has total size 94853 because it contains files f (size 29116), g(size 2557),
        and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
      - Directory d has total size 24933642.
      - As the outermost directory, / contains every file. Its total size is 48381165, the sum of
        the size of every file.

    To begin, find all of the directories with a total size of at most 100000, then calculate the
    sum of their total sizes. In the example above, these directories are a and e; the sum of their
    total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than
    once!)

    Find all of the directories with a total size of at most 100000. What is the sum of the total
    sizes of those directories?
    """
    root = make_filesystem(commands)
    sum_of_sizes = 0
    for node in flatten_filesystem(root):
        if node.size <= 100000 and len(node.children) > 0:
            sum_of_sizes += node.size
    print(sum_of_sizes)


def main2(commands):
    """
    --- Part Two ---

    Now, you're ready to choose a directory to delete.

    The total disk space available to the filesystem is 70000000. To run the update, you need unused
    space of at least 30000000. You need to find a directory you can delete that will free up
    enough space to run the update.

    In the example above, the total size of the outermost directory (and thus the total amount of
    used space) is 48381165; this means that the size of the unused space must currently be
    21618835, which isn't quite the 30000000 required by the update. Therefore, the update still
    requires a directory with total size of at least 8381165 to be deleted before it can run.

    To achieve this, you have the following options:

      - Delete directory e, which would increase unused space by 584.
      - Delete directory a, which would increase unused space by 94853.
      - Delete directory d, which would increase unused space by 24933642.
      - Delete directory /, which would increase unused space by 48381165.

    Directories e and a are both too small; deleting them would not free up enough space. However,
    directories d and / are both big enough! Between these, choose the smallest: d, increasing
    unused space by 24933642.

    Find the smallest directory that, if deleted, would free up enough space on the filesystem to
    run the update. What is the total size of that directory?
    """
    root = make_filesystem(commands)
    free_space = 70000000 - root.size
    remaining_space_needed = 30000000 - free_space
    best_option = root
    for node in flatten_filesystem(root):
        if node.size >= remaining_space_needed and node.size < best_option.size:
            best_option = node
    print(best_option.size)


def flatten_filesystem(node):
    all_nodes = [node]
    for child in node.children:
        all_nodes.extend(flatten_filesystem(child))
    return all_nodes


def make_filesystem(commands):
    """
    commands = [(['cd, '/'], []),
                (['ls'], [Dir(name='a'),
                          File(name='b.txt', size='14848514'),
                          File(name='c.dat', size='8504156'), Dir(name='d')]),
                (['cd, 'a'], []),
                (['ls'], [Dir(name='e'),
                          File(name='f', size='29116'),
                          File(name='g', size='2557'),
                          File(name='h.lst', size='62596')]),
                (['cd, 'e'], []),
                (['ls'], [File(name='i', size='584')]),
                (['cd, '..'], []),
                (['cd, '..'], []),
                (['cd, 'd'], []),
                (['ls'], [File(name='j', size='4060174'),
                          File(name='d.log', size='8033020'),
                          File(name='d.ext', size='5626152'),
                          File(name='k', size='7214296')])]
    """
    root = Node('/')
    # We have no starting cwd, so we depend on the first command being 'cd /'
    for command, outputs in commands:
        if command[0] == 'cd':
            if command[1] == '/':
                cwd = root
            else:
                cwd = cwd.cd(command[1])
        elif command[0] == 'ls':
            for output in outputs:
                if isinstance(output, OutputDir):
                    cwd.mkdir(output.name)
                elif isinstance(output, OutputFile):
                    cwd.mkfile(output.name, output.size)
    return root


def parse(input):
    raw_commands = input.split('$ ')[1:]
    commands = []
    for raw_command_and_outputs in raw_commands:
        raw_command, *raw_outputs = raw_command_and_outputs.rstrip('\n').split('\n')
        command = raw_command.split(' ')
        commands.append((command, list(parse_outputs(raw_outputs))))
    return commands


def parse_outputs(raw_outputs):
    for raw_output in raw_outputs:
        a, b = raw_output.split(' ')
        if a == 'dir':
            yield OutputDir(name=b)
        else:
            yield OutputFile(name=b, size=int(a))


OutputDir = namedtuple('Dir', ['name'])
OutputFile = namedtuple('OutputFile', ['name', 'size'])


class Node:
    def __init__(self, name, size=0, parent=None):
        self.name = name
        self.size = size
        self.parent = parent
        self.children = []

    def __repr__(self):
        return f'Node({repr(self.name)}{", size=" + repr(self.size) if self.size else ""}{", parent=" + repr(self.parent) if self.parent else ""})'

    def __str__(self):
        if len(self.children) > 0:
            return f'N({self.name} [{", ".join([str(child) for child in self.children])}])'
        else:
            return f'N({self.name}{":" + str(self.size) if self.size is not None else ""})'

    def cd(self, dir):
        if dir == '..':
            return self.parent
        else:
            return self.find_child(dir)

    def mkdir(self, name):
        self.assert_child_not_yet_exists(name)
        new_child = Node(name, size=0, parent=self)
        self.children.append(new_child)
        return new_child

    def mkfile(self, name, size):
        self.assert_child_not_yet_exists(name)
        new_child = Node(name, size=size, parent=self)
        self.children.append(new_child)
        self.propagate_size_up(size)
        return new_child

    def find_child(self, name):
        matches = list(filter(lambda n: n.name == name, self.children))
        assert len(matches) == 1
        return matches[0]

    def assert_child_not_yet_exists(self, name):
        matches = list(filter(lambda n: n.name == name, self.children))
        assert len(matches) == 0

    def propagate_size_up(self, size):
        self.size += size
        if self.parent:
            self.parent.propagate_size_up(size)


def raw_input(filename):
    return open(filename, "r").read().rstrip("\n")


if __name__ == "__main__":
    with launch_ipdb_on_exception():
        filename = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "2":
            main2(parse(raw_input(filename)))
        else:
            main(parse(raw_input(filename)))
