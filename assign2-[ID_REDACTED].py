'''
Assignment 2 - Eric Anderson

Revision

1. The definition of the shortest path between two vertices in a weighted
graph is the path that has the lowest cost between the two vertices.

2. The main steps in Dijkstra's algorithm are the following:
a. Choose a starting vertex
b. Pick another open vertex adjacent to the starting vertex
that has the smallest cost
c. expand from that vertex to all of its neighbors that are not closed
d. for each neighbor that we reached, the cost of the edge to the neighbor is
added onto the cost for the vertex to get a new path cost for the neighbor.
e. If the path cost is lower than the previous one, or neighbor is new, update
the neighbors path cost
f. close the current vertex.
g. Repeat b-f until all vertices are closed

3. An adaptable priority queue is a queue where the priority of its elements
undergo changes. We would use it in Dijkstra's algorithm by using it to store all open
vertices, giving priority to the vertices with the lowest cost. The APQ
implementation would be best for use in Dijkstra in application to standard
road maps would be the heap APQ implementation.
'''
#Vertex, edge, and graph definitions
class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element

class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v,w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element

class Graph:
    """ Represent a simple graph.

    This version maintains only undirected graphs, and assumes no
    self loops.
    """

    #Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    #-----------------------------------------------------------------------#

    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])    # the dict of edges for v
        return num //2     # divide by 2, since each edege appears in the
                           # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                         and v in self._structure
                         and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    #----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v,w) in elist:
            self.add_edge(v,w,None)

    #---------------------------------------------------------------------#

    # Additional methods to explore the graph

    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv

    def depthfirstsearch(self, v):
        """ Return a DFS tree from v.

        Args:
            v - a vertex object
        """
        marked = {v: None}
        self._depthfirstsearch(v, marked)
        return marked

    def _depthfirstsearch(self, v, marked):
        """ Do a recursive DFS from v, storing nodes in a dictionary 'marked'.

        Args:
            v - a vertex object
            marked - a dictionary representing the DFS tree
        """
        for e in self.get_edges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthfirstsearch(w, marked)

    def breadthfirstsearch(self, v):
        marked = {v:None}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                edges = self.get_edges(w)
                for e in edges:
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = e
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def print_paths_and_distance(self, v):
        return None

    # End of class definition

#---------------------------------------------------------------------------#
# Element class for the AdaptablePriorityQueue - yanked from slides
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

    # Add method, where we add a new item into the priority queue with priority key,
    # and return its Element in the APQ
    def add(self, key, item):
        # create the Element with index of last place, add to heap
        # and bubble up, changing indices of Elts, return the Element
        endPos = len(self._elemList)
        element = Element(key, item, endPos)
        self._elemList.append(element)
        self.bubbleup(endPos)
        return element

    # Min method
    def min(self):
        # read first cell in array and return
        return self._elemList[0]

    # Remove min
    def remove_min(self):
        # swap first element into last place
        firstElement = self.min()
        self._elemList[0] = self._elemList[len(self._elemList)-1]
        self._elemList[len(self._elemList)-1] = firstElement
        # pop the element
        self._elemList.pop()
        # bubble top element down, changing indices (Done inside bubbledown)
        self.bubbledown(0, len(self._elemList)-1)
        #return popped key, value - the min element
        return firstElement

    # Get element method - used for debugging & methods
    def get_element(self, element):
        return self._elemList[element._index]

    # Gets element with provided value
    # Since the heap implementation puts elements not in order, linear search must be used.
    def get_element_by_value(self, value):
        for element in self._elemList:
            if element._value == value:
                return element
        return -1

    # Update key method
    def update_key(self, element, newkey):
        # update the element's key.
        oldKey = element._key
        element._key = newkey
        # if only one element, no need for comparison
        if len(self._elemList) != 1:
            # if key less than parent's key bubble up
            if newkey < oldKey:
                self.bubbleup(element._index)
            # else bubble down
            else:
                self.bubbledown(element._index, len(self._elemList))

    # Get key method
    def get_key(self, element):
        # return the element's key
        return element._key

    # Remove method
    def remove(self, element):
        # swap last element with one in element's index,
        self._elemList[element._index] = self._elemList[len(self._elemList)-1]
        self._elemList[len(self._elemList)-1] = element
        # pop the last element
        self._elemList.pop()
        # if swap key < parent, bubble up
        if self._elemList[element._index]._key < self._elemList[(i-1) // 2]._key:
            self.bubbleup(element._index)
        # else bubble down
        else:
            self.bubbledown(element._index, len(self.elemList)-1)
        return element._key, element._value

    # Bubble up method - taken from the sorting solutions with slight modifications
    # Used since the AdaptablePriorityQueue is supposed to be a heap implementation
    def bubbleup(self, i):
        """ Bubble up item currently in pos i in a min heap. """
        while i > 0:
            parent = (i-1) // 2
            if self._elemList[i]._key < self._elemList[parent]._key:
                # Here is where the indices are changed for each bubbleup call
                self._elemList[i], self._elemList[parent] = self._elemList[parent], self._elemList[i]
                self._elemList[i]._index, self._elemList[parent]._index  = self._elemList[parent]._index, self._elemList[i]._index
                i = parent
            else:
                i = 0

    # Bubble up method - taken from the sorting solutions
    # Again, used since the AdaptablePriorityQueue is supposed to be a heap implementation
    def bubbledown(self, i, last):
        """ Bubble down item currently in pos i in a min heap (stops at last). """
        while last > (i*2):  # so at least one child
            lc = i*2 + 1
            rc = i*2 + 2
            minc = lc   # start by assuming left child is the max child
            if last > lc and self._elemList[rc] < self._elemList[lc]:  #r c exists and is bigger
                minc = rc
            if self._elemList[i] > self._elemList[minc]:
                # Here is where the indices are changed for each bubbledown call
                self._elemList[i], self._elemList[minc] = self._elemList[minc], self._elemList[i]
                self._elemList[i]._index, self._elemList[minc]._index = self._elemList[minc]._index, self._elemList[i]._index
                i = minc
            else:
                i = last


#Djkstra's algorithm implementation (i)
def Dijkstra(graph, startVertex):
    # open starts as an empty APQ
    open = AdaptablePriorityQueue()
    # locs is an empty dictionary (keys are vertices, values are location in open)
    locs = dict()
    # closed starts as an empty dictionary
    closed = dict()
    # preds starts as a dictionary with value for s = None
    # s corresponds to startVertex in this case
    preds = {startVertex:None}
    # add s with APQ key 0 to open, and add s:(elt returned from APQ) to locs
    startElement = open.add(0, startVertex)
    locs[startVertex] = startElement
    # while open is not empty
    while not open._elemList == []:
        # remove the min element v and its cost (key) from open
        min = open.remove_min()
        v = min._value
        cost = min._key
        # remove the entry for v from locs and preds (which returns predecessor)
        rmminInLoc = locs.pop(v)
        rmminInPred = preds.pop(v)
        # add an entry for v:(cost, predecessor) into closed
        closed[v] = (cost, rmminInPred)
        # for each edge e from v
        for edge in graph.get_edges(v):
            # w is the opposite vertex to v in e
            # w corresponds to opposVertex in this case
            opposVertex = edge.opposite(v)
            opposVertex_element = open.get_element_by_value(opposVertex)
            # if w is not in closed
            if opposVertex not in closed:
                # newcost is v's key plus e's cost
                newcost = cost + edge._element
                # if w is not in locs i.e. not yet added into open
                if opposVertex not in locs.keys():
                    # add w:v to preds, add w:newcost to open, add w:(elt returned from open) to locs
                    preds[opposVertex] = min
                    newElement = open.add(newcost, opposVertex)
                    locs[opposVertex] = newElement
                # else if newcost is better than w's oldcost
                elif newcost < opposVertex_element._key:
                    # update w:v in preds, update w's cost in open to newcost
                    preds.update({opposVertex:min})
                    open.update_key(opposVertex_element, newcost)
    return closed

# Path printing function
def print_path(path):
    #Iterating through the path
    for key in path:
        # print(key, path[key]) # -> 2 (3.0, <AdaptablePriorityQueue.Element object at 0x7f6bff599160>)
        # Checking to see if we are at the start or not
        if path[key][1] is not None:
            # Printing the key vertex, cost of path, and previous vertex
            print(str(key) + ' -> (' + str(path[key][0]) + ", " + str(path[key][1]._value) + ')')
        else:
            # Printing the starting vertex
            print(str(key) + ' -> Starting Vertex')

# Graph reader function (Taken from Lab documentation)
def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

'''
#Code used to test graph implementation
graph1 = graphreader('simplegraph1.txt')
start1 = get_vertex_by_label(1)
end1 = get_vertex_by_label(4)
graph2 = graphreader('simplegraph2.txt')
start2 = get_vertex_by_label(14)
end2 = get_vertex_by_label(5)
'''

'''
#Code used to test AdaptablePriorityQueue and element implementations
testElement1 = Element(10, 'Dr Wily', 0)
testElement2 = Element(15, 'Dr Light', 2)
print("One element is known as " + testElement1._value + ' with key ' + str(testElement1._key) + ' at index ' + str(testElement1._index))
print("Another element is known as " + testElement2._value + ' with key ' + str(testElement2._key) + ' at index ' + str(testElement2._index))

testAPQ = AdaptablePriorityQueue()
testAPQ.add(800, 'Mega Man')
testAPQ.add(100, 'Cut Man')
testAPQ.add(200, 'Guts Man')
testAPQ.add(300, 'Ice Man')
testAPQ.add(400, 'Bomb Man')
testAPQ.add(500, 'Fire Man')
testAPQ.add(600, 'Elec Man')
for element in testAPQ._elemList:
    print('Element ' + str(element._index) + ' is known as ' + element._value + ' with key ' + str(element._key))
'''

# Reading the graphs and using 1 as the starting vertex
graph1 = graphreader('simplegraph1.txt')
start1 = graph1.get_vertex_by_label(1)
graph2 = graphreader('simplegraph2.txt')
start2 = graph2.get_vertex_by_label(1)

# Using Dijkstra on the Graphs
graph_paths =  Dijkstra(graph1, start1)
graph_paths2 = Dijkstra(graph2, start2)

# Printing the paths
print("Shortest paths of graph 1 starting from vertex %d" % start1._element)
print("Format is: (Vertex) -> ((Vertex Path Cost), (Previous Vertex)")
print_path(graph_paths)
print("Shortest paths of graph 2 starting from vertex %d" % start2._element)
print("Format is: (Vertex) -> ((Vertex Path Cost), (Previous Vertex)")
print_path(graph_paths2)
