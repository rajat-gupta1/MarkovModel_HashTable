from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self.capacity = capacity
        self._items = [None] * self.capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.length = 0
        self.n = 0

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
        
        if self.length + 1 > self.capacity * self.load_factor:
            self.length = 0
            self.capacity *= self.growth_factor
            temp = self._items.copy()
            self._items = [None] * self.capacity
            for item in temp:
                if item != None and item[2] != 'del':
                    self.length += 1
                    hashval = self._hash(item[0])
                    while(self._items[hashval] != None):
                        hashval = (hashval + 1) % self.capacity
                    self._items[hashval] = (item[0], item[1], 'in')

        self.length += 1
        hashval = self._hash(key)
        while(self._items[hashval] != None and self._items[hashval][2] != 'del'):
            if self._items[hashval][0] == key:
                self.length -= 1
                break
            hashval = (hashval + 1) % self.capacity
        self._items[hashval] = (key, val, 'in')

    def __getitem__(self, key):
        hashval = self._hash(key)
        if self._items[hashval] == None:
            return self.default_value
        while(self._items[hashval][0] != key):
            if self._items[hashval] != None:
                hashval = (hashval + 1) % self.capacity
            if self._items[hashval] == None:
                return self.default_value
        if self._items[hashval][2] != 'del':
            return self._items[hashval][1]
        return self.default_value

    def __delitem__(self, key):
        hashval = self._hash(key)
        if self._items[hashval] == None:
            raise KeyError
        while(self._items[hashval][0] != key):
            if self._items[hashval] != None:
                hashval = (hashval + 1) % self.capacity
            if self._items[hashval] == None:
                raise KeyError
        
        if self._items[hashval][2] == 'del':
                raise KeyError

        self._items[hashval] = (self._items[hashval][0], 
        self._items[hashval][1], 'del')
        self.length -= 1

    def __len__(self):
        return self.length

    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        # raise NotImplementedError("__iter__ not implemented")
        self.n = 0
        return self

    def __next__ (self):
        if self.n < self.capacity:
            result = self.n
            self.n += 1
            return result
        raise StopIteration