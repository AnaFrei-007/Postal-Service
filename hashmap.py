class HashMap:
    def __init__(self, capacity=45):
        self.table = []
        for _ in range(capacity):
            self.table.append([])

    def insert(self, key, value):
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        # If the key already exists in the bucket, update its value
        for entry in bucket:  # O(N) time complexity
            if entry[0] == key:
                entry[1] = value
                return True

        # If the key is not found, append the key-value pair to the bucket
        bucket.append([key, value])
        return True

    # Look up an item from the hash table using the key
    def lookup(self, key):
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        # Search for the key in the corresponding bucket
        for entry in bucket:
            if entry[0] == key:
                return entry[1]

        return None  # Return None if the key is not found

    def remove(self, key):
        index = hash(key) % len(self.table)
        bucket = self.table[index]

        # If the key exists in the bucket, remove the entry
        for entry in bucket:
            if entry[0] == key:
                bucket.remove(entry)
                return True
        return False

    def __repr__(self):
        s = "   --------\n"
        index = 0
        for item in self.table:
            value = str(item)
            if not item:
                value = 'E'
            s += '{:2}:|{:^6}|\n'.format(index, value)
            index += 1
        s += "   --------"
        return s

