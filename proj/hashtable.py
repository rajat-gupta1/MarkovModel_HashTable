from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    """
    This class creates a hashtable, using Horner's rule and the size of the
    base table for hashing will dynamically increase if the size of elements
    is more than the capcacity defined initially times the load factor
    """

    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self.capacity = capacity

        # Initialising all elements in the table to None
        self._items = [None] * self.capacity

        # Default value to return in case we dont find the element in the table
        self.default_value = default_value

        # If capacity times load factor is greater than elements present, we
        # increase the size of the table
        self.load_factor = load_factor

        # The factor to increase the size of the table by
        self.growth_factor = growth_factor

        # Number of elements currently present in the table
        self.length = 0

        # For iterating through the table
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

    def rehash(self):
        """
        If the number of elements in the table has increased beyond capacity
        times load factore, we will rehash the table, by increasing its size. 
        This function is called when the table is to be rehashed
        """

        self.length = 0
        self.capacity *= self.growth_factor

        # Creating a copy of the current table, because we will need to change
        # the table while rehashing
        temp = self._items.copy()
        self._items = [None] * self.capacity
        for item in temp:

            # Checking if the item was not none and wasnt deleted earlier
            if item != None and item[2] != 'del':
                self.length += 1

                # Regenerating hashvalue for this item
                hashval = self._hash(item[0])
                while(self._items[hashval] != None):
                    hashval = (hashval + 1) % self.capacity
                self._items[hashval] = (item[0], item[1], 'in')

    def __setitem__(self, key, val):
        """
        For adding an item to the hash table basis a key and value
        """
        
        if self.length + 1 > self.capacity * self.load_factor:
            self.rehash()

        self.length += 1
        hashval = self._hash(key)
        while(self._items[hashval] != None and self._items[hashval][2] != 'del'):

            # If the key is already present, we will update its value
            if self._items[hashval][0] == key:
                self._items[hashval] = (key, val, 'in')

                # Because size of the table shouldnt change in this case
                self.length -= 1
                break
            hashval = (hashval + 1) % self.capacity
        self._items[hashval] = (key, val, 'in')

    def check_item (self, key, get_del):
        """
        Helper function for get and del values. This function checks if a value
        if present in the given table. 
        """

        hashval = self._hash(key)

        if self._items[hashval] == None:

            # returning default value if the the function was called from get
            if get_del == 'get':
                return (1, self.default_value)

            # Raising keyerror if the function was called from delete
            raise KeyError

        while(self._items[hashval][0] != key):
            if self._items[hashval] != None:
                hashval = (hashval + 1) % self.capacity
            if self._items[hashval] == None:
                if get_del == 'get':
                    return (1, self.default_value)
                raise KeyError
        return hashval

    def __getitem__(self, key):
        hashval = self.check_item(key, 'get')

        # In case default value was returned from the helper function
        if type(hashval) is tuple:
            return hashval[1]

        if self._items[hashval][2] != 'del':
            return self._items[hashval][1]
        return self.default_value

    def __delitem__(self, key):
        hashval = self.check_item(key, 'del')

        # If the item was already deleted
        if self._items[hashval][2] == 'del':
            raise KeyError

        self._items[hashval] = (self._items[hashval][0], 
        self._items[hashval][1], 'del')
        self.length -= 1

    def __len__(self):
        """
        Modifying the len dunder method to return the number of elements in the
        hashtable
        """

        return self.length

    def __iter__(self):
        """
        To iterate through the hashtable
        """

        # Initialising n with 0, for next to iterate through it
        self.n = 0
        return self

    def __next__ (self):
        """
        To iterate through the hashtable
        """

        # Iterating only till the capacity
        if self.n < self.capacity:
            result = self.n
            self.n += 1
            return result
        raise StopIteration