"""
CSCI-603: Graphs
Author: Sean Strout @ RIT CS
Author: Pavan Prabhakar Bhat (pxb8715@rit.edu)

An implementation of a graph data structure as an adjacency list.

Code taken from the online textbook and modified:

http://interactivepython.org/runestone/static/pythonds/Graphs/Implementation.html
"""

import sys  # argv
import collections
import os.path
import math

maxScore = 0
score = 0
color = 0
cows = []
cows1 = []
cowColors = []
cowColors1 = []
current = []

class Graph:
    """
    A graph implemented as an adjacency list of vertices.

    :slot: vertList (dict):  A dictionary that maps a vertex key to a Vertex
        object
    :slot: numVertices (int):  The total number of vertices in the graph
    """

    __slots__ = 'vertList', 'numVertices', 'srcFile'

    def __init__(self, srcFile):
        """
        Initialize the graph
        :return: None
        """
        self.vertList = {}
        self.numVertices = 0
        self.srcFile = srcFile

    def addVertex(self, key):
        """
        Add a new vertex to the graph.
        :param key: The identifier for the vertex (typically a string)
        :return: Vertex
        """
        # count this vertex if not already present
        if self.getVertex(key) == None:
            self.numVertices += 1
        vertex = Vertex(key)
        self.vertList[key] = vertex
        return vertex

    def getVertex(self, key):
        """
        Retrieve the vertex from the graph.
        :param key: The vertex identifier
        :return: Vertex if it is present, otherwise None
        """
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None

    def __contains__(self, key):
        """
        Returns whether the vertex is in the graph or not.  This allows the
        user to do:

            key in graph

        :param key: The vertex identifier
        :return: True if the vertex is present, and False if not
        """
        return key in self.vertList

    def addEdge(self, src, dest, cost=0):
        """
        Add a new directed edge from a source to a destination of an edge cost.
        :param src: The source vertex identifier
        :param dest: The destination vertex identifier
        :param cost: The edge cost (defaults to 0)
        :return: None
        """
        if src not in self.vertList:
            self.addVertex(src)
        if dest not in self.vertList:
            self.addVertex(dest)
        self.vertList[src].addNeighbor(self.vertList[dest], cost)

    def getVertices(self):
        """
        Return the collection of vertex identifiers in the graph.
        :return: A list of vertex identifiers
        """
        return self.vertList.keys()

    def __iter__(self):
        """
        Return an iterator over the vertices in the graph.  This allows the
        user to do:

            for vertex in graph:
                ...

        :return: A list iterator over Vertex objects
        """
        return iter(self.vertList.values())

    def beginSimulation(self, keys, values, start=""):
        """
        This function is used to begin simulation of the graph.
        :param keys: Holds the paint balls used to paint the cows or to trigger different paint balls
        :param values: Holds the cows and other colors that can be triggered
        :param start: Starting value from which the triggering of a paint ball will begin
        :return: Score as to how many cows were painted by a single paint ball
        """
        # global constants
        global score, cows, cowColors, maxScore, cows1, cowColors1, current

        for i in range(len(keys)):
            if start == keys[i].vertexName and values[i].vertexType == 'cow':
                print('\t', values[i].vertexName, 'is painted', start + '!')
                cows.append(values[i].vertexName)
                cowColors.append(start)
                score += 1
            elif start == keys[i].vertexName:
                print('\t', values[i].vertexName, 'paint ball is triggered by', start, 'paint ball')
                print(current, values[i].vertexName)
                if values[i].vertexName not in current:
                    self.beginSimulation(keys, values, values[i].vertexName)
        return score

class Vertex:
    """
    An individual vertex in the graph.

    :slots: id:  The identifier for this vertex (user defined, typically
        a string)
    :slots: connectedTo:  A dictionary of adjacent neighbors, where the key is
        the neighbor (Vertex), and the value is the edge cost (int)
    """

    __slots__ = 'id', 'connectedTo'

    def __init__(self, key):
        """
        Initialize a vertex
        :param key: The identifier for this vertex
        :return: None
        """
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        """
        Connect this vertex to a neighbor with a given weight (default is 0).
        :param nbr (Vertex): The neighbor vertex
        :param weight (int): The edge cost
        :return: None
        """
        self.connectedTo[nbr] = weight

    def __str__(self):
        """
        Return a string representation of the vertex and its direct neighbors:

            vertex-id connectedTo [neighbor-1-id, neighbor-2-id, ...]

        :return: The string
        """
        return str(self.id) + ' connectedTo: ' + str([str(x.id) for x in self.connectedTo])

    def getConnections(self):
        """
        Get the neighbor vertices.
        :return: A list of Vertex neighbors
        """
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        """
        Get the edge cost to a neighbor.
        :param nbr (Vertex): The neighbor vertex
        :return: The weight (int)
        """
        return self.connectedTo[nbr]



def main():
    """
    A main function for the Graph class.
    :return: None
    """
    # Checks if the number of arguments entered through the command line are appropriate or exits
    if len(sys.argv) != 3:
        print('Usage: python3 holicow.py source-file.txt')
        sys.exit(0)

    # Holds temporary values of the vertices
    tempVertices = []
    # Holds the index of the list which is read from the file
    count = 0
    # Holds the details of the vertices temporarily before inputting the named tuple
    list1 = []
    # A temporary list that holds the vertices in the form of a named tuple
    vertex = collections.namedtuple('Vertices', ['vertexType', 'vertexName', 'x', 'y', 'splatterRadius'])
    # Holds the paint balls that are supposed to trigger
    keys = []
    # Holds the color or the cow which is being triggered by another color held in keys
    values = []
    # Holds a list of names of cows on the field
    listOfCows = []
    # Global constants used
    global maxScore, score, color, cows, cows1, cowColors, cowColors1, current
    # object of class Graph
    graph = Graph(sys.argv[2])
    try:
        # File contains the appropriate file contents
        file = open(sys.argv[2])
    except IOError:
        # Handles the exception if the file is not found
        print("File Not Found: ", sys.argv[2])
        sys.exit(0)

    print('Field of Dreams')
    print('---------------')
    for l in file:
        if l.find("paintball") :
            s = l.split()
            list1.append(s)
            # Contains the list of cows in the field
            listOfCows.append(list1[count][1])
            # Contains cows
            tempVertices.append(vertex(list1[count][0], list1[count][1], float(list1[count][2]), \
                                       float(list1[count][3]), float(0)))
            count += 1
        elif l.find("cow"):
            s = l.split()
            list1.append(s)
            # Contains paint balls
            tempVertices.append(vertex(list1[count][0], list1[count][1], float(list1[count][2]), \
                                       float(list1[count][3]), float(list1[count][4])))
            count += 1
        else:
            print('Unknown input')

    for i in range(len(tempVertices)):
        if(tempVertices[i].vertexType == 'paintball'):
            for j in range(len(tempVertices)):
                if ( i is not j):
                    # Distance formula to calculate the distance from the neighbouring vertices
                    distance = math.sqrt(((tempVertices[j][2] - tempVertices[i][2]) ** 2)  \
                                        + ((tempVertices[j][3] - tempVertices[i][3]) ** 2))
                    if(distance <= tempVertices[i][4]):
                        # adds the edges of the graph
                        graph.addEdge(tempVertices[i].vertexName, tempVertices[j].vertexName)
                        # appends the paint balls and the colors and cows triggered by it
                        keys.append(tempVertices[i])
                        values.append(tempVertices[j])
    # Displays the field through the connections of each vertice
    for i in graph:
        print(i)
    # contains the paint balls to be triggered
    paintballs = []
    #  contains the score of the paint balls
    paintballScore = []
    a = 0

    print()
    print('Beginning simulation...')
    for j in range(len(tempVertices)):
        score = 0
        if(tempVertices[j].vertexType == 'paintball'):
            print('Triggering', tempVertices[j].vertexName, 'paint ball...')
            current[:] = []
            current.append(tempVertices[j].vertexName)
            paintballs.append(tempVertices[j].vertexName)
            start = tempVertices[j].vertexName
            paintballScore.append(graph.beginSimulation(keys, values, start))
            # check for the list of cows to be colored
            if len(cows) > len(cows1):
                cows1 = cows
                cowColors1 = cowColors
            cows = []
            cowColors = []


    temp = max(paintballScore)

    for i in range(len(paintballScore)):
        if temp == paintballScore[i]:
            a = i
            break

    print()
    print('Results:')
    if paintballScore[a] == 0:
        print("No cows were painted by any starting paint ball!")
    else:
        print('Triggering the', paintballs[a], 'paint ball is the best choice with', paintballScore[a],\
          'total paint on the cows:')
        cowColor = {}

        # forms a dictionary of cows and their paints

        for i in range(len(cows1)):
            if cows1[i] not in cowColor:
                cowColor[cows1[i]] = [cowColors1[i]]
            elif cowColors1[i] not in cowColor[cows1[i]]:
                cowColor[cows1[i]].append(cowColors1[i])


        for j in cowColor.items():
            print('\t'+j[0]+"'s colors: {" + str(j[1])[1: len(str(j[1]))-1] + "}")

        for l in listOfCows:

            if l not in [k[0] for k in cowColor.items()]:
                print('\t' + l + "'s colors: {" + "}")

if __name__ == '__main__':
    main()
