import Graph_Library as gr

def initPersonalMap(graph):
    graph.AddCrossing("A")
    graph.AddCrossing("B")
    graph.AddCrossing("C")
    graph.AddCrossing("D")
    graph.AddCrossing("F")
    graph.AddCrossing("G")
    graph.AddCrossing("H")
    graph.AddCrossing("I")
    graph.AddReachableCrossingToCrossing("A", "B", 50.5, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("B", "C", 47.2, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("A", "D", 63.7, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("B", "E", 64, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("C", "F", 64.3, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("D", "E", 51.8, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("E", "F", 46.3, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("D", "G", 43.3, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("F", "I", 43.5, False, gr.Direction.South)
    graph.AddReachableCrossingToCrossing("G", "H", 51.8, False, gr.Direction.East)
    graph.AddReachableCrossingToCrossing("H", "I", 46.5, False, gr.Direction.East)

    return graph
