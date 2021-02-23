#from zumi.zumi import Zumi
import Graph as gr

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

    graph.AddReachableCrossingToCrossing("S", "A", 5, False, gr.Direction.North)
    graph.AddReachableCrossingToCrossing("S", "B", 2, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("S", "G", 4, False, gr.Direction.East)

    graph.AddReachableCrossingToCrossing("A", "B", 1, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("A", "C", 3, False, gr.Direction.North)

    graph.AddReachableCrossingToCrossing("B", "C", 8, False, gr.Direction.South)

    graph.AddReachableCrossingToCrossing("G", "D", 2, False, gr.Direction.East)

    graph.AddReachableCrossingToCrossing("C", "D", 4, False, gr.Direction.North)
    graph.AddReachableCrossingToCrossing("C", "E", 6, False, gr.Direction.South)

    graph.AddReachableCrossingToCrossing("D", "E", 10, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("D", "F", 8, False, gr.Direction.North)

    graph.AddReachableCrossingToCrossing("E", "Z", 7, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("F", "Z", 11, False, gr.Direction.East)

    return graph
