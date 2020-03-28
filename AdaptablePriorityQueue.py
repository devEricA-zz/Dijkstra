# Element class for the AdaptablePriorityQueue
class Element:
    """ A key, value and index. """
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i
    def __eq__(self, other):
        return self._key == other._key
    def __lt__(self, other):
        return self._key < other._key
    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None


# AdaptablePriorityQueue Class, to be used in the Dijkstra's algorithm
class AdaptablePriorityQueue:
    # Element list constructor
    def __init__(self, elemList):
        self._elemList = elemList
    # Empty list constructor
    def __init__(self):
        self._elemList = []

    # Add method
    def add(self, key, item):
        endPos = len(self._elemList)
        element = Element(key, item, endPos)
        self._elemList.append(element)
        self.bubbleup(endPos)
        return element

    # Min method
    def min(self):
        return self._elemList[0]

    # Remove min
    def remove_min(self):
        firstElement = self.min()
        self._elemList[0] = self._elemList[len(self._elemList)-1]
        self._elemList[len(self._elemList)-1] = firstElement
        self._elemList.pop()
        self.bubbledown(0, len(self._elemList)-1)
        return firstElement

    # Get element method - used for debugging & methods
    def get_element(self, element):
        return self._elemList[element._index]

    #Gets element with provided value
    def get_element_by_value(self, value):
        for element in self._elemList:
            if element._value == value:
                return element
        return -1


    # Update key method
    def update_key(self, element, newkey):
        oldKey = element._key
        element._key = newkey
        if len(self._elemList) != 1:
            if newkey < oldKey:
                self.bubbleup(element._index)
            else:
                self.bubbledown(element._index, len(self._elemList))

    # Get key method
    def get_key(self, element):
        return element._key

    # Remove method
    def remove(self, element):
        self._elemList[element._index] = self._elemList[len(self._elemList)-1]
        self._elemList[len(self._elemList)-1] = element
        self._elemList.pop()
        if self._elemList[element._index]._key < self._elemList[(i-1) // 2]._key:
            self.bubbleup(element._index)
        else:
            self.bubbledown(element._index, len(self.elemList)-1)

    # Bubble up method - taken from the sorting solutions
    # Used since the AdaptablePriorityQueue is supposed to be a heap implementation
    def bubbleup(self, i):
        """ Bubble up item currently in pos i in a min heap. """
        while i > 0:
            parent = (i-1) // 2
            if self._elemList[i]._key < self._elemList[parent]._key:
                self._elemList[i], self._elemList[parent] = self._elemList[parent], self._elemList[i]
                self._elemList[i]._index, self._elemList[parent]._index  = self._elemList[parent]._index, self._elemList[i]._index
                i = parent
            else:
                i = 0

    # Bubble up method - taken from the sorting solutions
    def bubbledown(self, i, last):
        """ Bubble down item currently in pos i in a min heap (stops at last). """
        while last > (i*2):  # so at least one child
            lc = i*2 + 1
            rc = i*2 + 2
            minc = lc   # start by assuming left child is the max child
            if last > lc and self._elemList[rc] < self._elemList[lc]:  #r c exists and is bigger
                minc = rc
            if self._elemList[i] > self._elemList[minc]:
                #print('swapping:', inlist[i], 'with its child:', inlist[maxc])
                self._elemList[i], self._elemList[minc] = self._elemList[minc], self._elemList[i]
                self._elemList[i]._index, self._elemList[minc]._index = self._elemList[minc]._index, self._elemList[i]._index
                i = minc
            else:
                i = last
