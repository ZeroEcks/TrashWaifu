import random


class Leaf:
    MIN_LEAF_SIZE = 6

    leftChild = None
    rightChild = None
    room = None
    halls = None

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def split(self):
        if self.leftChild or self.rightChild:
            return False

        horizontal_split = random.random() > 0.5
        if self.width > self.height and self.width / self.height >= 1.25:
            horizontal_split = False
        elif self.height > self.width and self.height / self.width >= 1.25:
            horizontal_split = True

        max_size = (self.height if horizontal_split else self.width) - self.MIN_LEAF_SIZE
        if max_size <= self.MIN_LEAF_SIZE:
            return False

        split = random.randrange(self.MIN_LEAF_SIZE, max_size)

        if horizontal_split:
            self.leftChild = Leaf(self.x, self.y, self.width, split)
            self.rightChild = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.leftChild = Leaf(self.x, self.y, split, self.height)
            self.rightChild = Leaf(self.x + split, self.y, self.width - split, self.height)

        return True

    def has_split(self):
        return self.leftChild or self.rightChild

    def collides(self, x, y):
        if self.x <= x < self.x + self.width:
            if self.y <= y < self.y + self.height:
                return True
        return False

    def is_wall(self, x, y):
        return self.x == x or self.x + self.width - 1 == x or self.y == y or self.y + self.height - 1 == y


class Generator:
    leaves = []

    def __init__(self, width, height, max_leaf_size=20):
        self.max_leaf_size = max_leaf_size
        self.width = width
        self.height = height
        self.leaves.clear()

        self.root_leaf = Leaf(0, 0, self.width, self.height)

        self.leaves.append(self.root_leaf)

        split_hasnt_failed = True
        while split_hasnt_failed:
            split_hasnt_failed = False
            for leaf in self.leaves:
                if not leaf.has_split():
                    if leaf.width > self.max_leaf_size or leaf.height > self.max_leaf_size or random.random() > 0.25:
                        if leaf.split():
                            self.leaves.append(leaf.leftChild)
                            self.leaves.append(leaf.rightChild)
                            split_hasnt_failed = True

    def export_array_grid(self):
        grid = list()
        for x in range(self.width):
            row = list()
            for y in range(self.height):
                for leaf in self.leaves:
                    if leaf.collides(x, y):
                        row.append(1 if leaf.is_wall(x, y) else 0)
            grid.append(row)
        return grid