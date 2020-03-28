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
import sys
# Imports all graph ADT's from the file that houses them
from Graph_Classes import *
#Imports AdaptablePriorityQueue and element classes
from AdaptablePriorityQueue import *

#Djkstra's algorithm implementation (i)
def Dijkstra(graph, startVertex, endVertex):
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
    # return closed
    # but we want a specific shortest path, not all of the shortest paths
    return traverse(closed, endVertex)

# Helper function used to get a specific path of the Dijkstra path
def traverse(closed_dict, target_vertex):
    # The targeted path starts empty
    target_path = dict()
    # Initially, the end vertex passed from the Dijkstra function is added
    # to the targeted path
    vertexDataToAdd = closed_dict.pop(target_vertex)
    target_path[target_vertex] = vertexDataToAdd
    # This while works backwards from the end vertex, adding all of the other vertexes
    while vertexDataToAdd[1] is not None:
        target_vertex = vertexDataToAdd[1]._value
        vertexDataToAdd = closed_dict.pop(target_vertex)
        target_path[target_vertex] = vertexDataToAdd
    # Once the path is acquired, we return it.
    return target_path

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
graph1 = graphreader('simplegraph1.txt')
start1 = graph1.get_vertex_by_label(1)
end1 = graph1.get_vertex_by_label(4)
graph2 = graphreader('simplegraph2.txt')
start2 = graph2.get_vertex_by_label(1)
end2 = graph2.get_vertex_by_label(5)

graph_path = Dijkstra(graph1, start1, end1)
#graph_path2 = Dijkstra(graph2, start2, end2)
print("PATH OF GRAPH 1 (VERTEX -> PREDECESSOR)")
for key in graph_path:
    try:
        print(str(key) + ' -> (' + str(graph_path[key][0]) + ", " + str(graph_path[key][1]._value) + ')')
    except:
        print(str(key) + ' -> (' + str(graph_path[key][0]) + ", " + str(graph_path[key][1]) + ')')

'''
print("PATH OF GRAPH 2")
for key in graph_path2:
    try:
        print(str(key) + ' -> (' + str(graph_path2[key][0]) + ", " + str(graph_path2[key][1]._value) + ')')
    except:
        print(str(key) + ' -> (' + str(graph_path2[key][0]) + ", " + str(graph_path2[key][1]) + ')')
'''