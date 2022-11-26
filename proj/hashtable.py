from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self._items = []

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value
        between 0 and self.capacity.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val % self.capacity

    def __setitem__(self, key, val):
        pass

    def __getitem__(self, key):
        pass

    def __delitem__(self, key):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")
