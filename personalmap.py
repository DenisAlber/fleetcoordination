#from zumi.zumi import Zumi
from Graph_Library import Direction as direction

def initPersonalMap(graph):
    graph.AddCrossing("S")
    graph.AddCrossing("A")
    graph.AddCrossing("B")
    graph.AddCrossing("G")
    graph.AddCrossing("C")
    graph.AddCrossing("D")
    graph.AddCrossing("E")
    graph.AddCrossing("F")
    graph.AddCrossing("Z")

    graph.AddReachableCrossingToCrossing("S", "A", 5, False, direction.North)
    graph.AddReachableCrossingToCrossing("S", "B", 2, False, direction.South)
    graph.AddReachableCrossingToCrossing("S", "G", 4, False, direction.East)

    graph.AddReachableCrossingToCrossing("A", "B", 1, False, direction.East)
    graph.AddReachableCrossingToCrossing("A", "C", 3, False, direction.North)

    graph.AddReachableCrossingToCrossing("B", "C", 8, False, direction.South)

    graph.AddReachableCrossingToCrossing("G", "D", 2, False, direction.East)

    graph.AddReachableCrossingToCrossing("C", "D", 4, False, direction.North)
    graph.AddReachableCrossingToCrossing("C", "E", 6, False, direction.South)

    graph.AddReachableCrossingToCrossing("D", "E", 10, False, direction.East)
    graph.AddReachableCrossingToCrossing("D", "F", 8, False, direction.North)

    graph.AddReachableCrossingToCrossing("E", "Z", 7, False, direction.South)
    graph.AddReachableCrossingToCrossing("F", "Z", 11, False, direction.East)

    return graph
