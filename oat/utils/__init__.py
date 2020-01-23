class DisjointSet():
    def __init__(self, value):
        self.value = value
        self.parent = self
        self.rank = 0

    def __repr__(self):
        return "{} <- {}".format(self.parent.value, self.value)


class DisjointSetForest():
    def __init__(self):
        self.forest = {}

    def make_set(self, item):
        """ Create a new set containing 'item' with representative 'item'

        We assume that item is not part of any existing set.
        """
        new_set = DisjointSet(item)
        self.forest[item] = new_set
        return new_set

    def find(self, item):
        """ Return the representative of the Set which contains 'item'

        Use path compression to improve running time.
        """

        if type(item) != DisjointSet:
            item = self.forest[item]
        if item != item.parent:
            item.parent = self.find(item.parent)
        return item.parent

    def union(self, item1, item2):
        """ Combine two disjoint sets by linking their representatives"""
        self._link(self.find(item1), self.find(item2))

    def _link(self, item1, item2):
        """ Link sets using the rank heuristic to improve running time"""
        if item1.rank > item2.rank:
            item2.parent = item1
        else:
            item1.parent = item2
            if item1.rank == item2.rank:
                item2.rank += 1

    def connected(self, item1, item2):
        if self.find(item1) == self.find(item2):
            return True
        else:
            return False

    def __repr__(self):
        sets = {}
        for s in self.forest:
            root = self.find(s).value
            if root not in sets.keys():
                sets[root] = [s.value]
            else:
                sets[root].append(s.value)
        return str(sets)

