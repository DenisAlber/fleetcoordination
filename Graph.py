from py_linq import Enumerable

class Graph:
    crossings = []
        
    def AddCrossing(self, crossingName):
        self.crossings.append(Crossing(crossingName))

    def PrintAllCrossingNamesAndReachableCrossings(self):
        for x in self.crossings:
            print("Knoten: " + x.crossingName)
            x.PrintReachableCrossings()
        

    def AddReachableCrossingToCrossing(self, crossingName, neighborCrossingName, weight, isOneWayStreet):
        """
            Fügt eine Kreuzung zur Liste mit den benachbarten Kreuzungen hinzu.
            
            Wenn die Straßen zwischen zwei Kreuzungen eine Einbahnstraße (isOneWayStreet = True) ist, 
            ist darauf zu achten das die Straße nur von crossingName zu neighborCrossingName befahren werden kann.
            Bsp.: AddReachableCrossingToCrossing("A","B","5",True) - Straße kann nur von A nach B befahren werden.
        """
        for x in self.crossings:
            if x.crossingName == crossingName:
                for o in self.crossings:
                    if o.crossingName == neighborCrossingName:
                        x.AddReachableCrossing(o, weight)
                        if isOneWayStreet == True: 
                            return
                        o.AddReachableCrossing(x, weight)
                        break
                break



class Crossing:
    def __init__(self, crossingName):
        self.crossingName = crossingName
        self.reachableCrossings = []
        self.currentWeight = float('inf')

    def AddReachableCrossing(self, crossing, weight):
        # check if neighbor already exists
        for x in self.reachableCrossings:
            if(x.crossing == crossing):
                return
        # add neighbor to crossing
        self.reachableCrossings.append(ReachableCrossing(crossing, weight))
    
    def PrintReachableCrossings(self):
        print('\tBenachbart Kreuzungen:', end=" ")
        print(Enumerable(self.reachableCrossings).select(lambda x: x.crossing.crossingName))

class ReachableCrossing:
    def __init__(self, crossing, weight):
        self.crossing = crossing
        self.weight = weight


    


g = Graph()
g.AddCrossing("S")
g.AddCrossing("A")
g.AddCrossing("B")
g.AddCrossing("G")
g.AddCrossing("C")
g.AddCrossing("D")
g.AddCrossing("E")
g.AddCrossing("F")
g.AddCrossing("Z")

g.AddReachableCrossingToCrossing("S", "A", 5, False)
g.AddReachableCrossingToCrossing("S", "B", 2, False)
g.AddReachableCrossingToCrossing("S", "G", 4, False)

g.AddReachableCrossingToCrossing("A", "B", 1, False)
g.AddReachableCrossingToCrossing("A", "C", 3, False)

g.AddReachableCrossingToCrossing("B", "C", 8, False)

g.AddReachableCrossingToCrossing("G", "D", 2, False)

g.AddReachableCrossingToCrossing("C", "D", 4, False)
g.AddReachableCrossingToCrossing("C", "E", 6, False)

g.AddReachableCrossingToCrossing("D", "E", 10, False)
g.AddReachableCrossingToCrossing("D", "F", 8, False)

g.AddReachableCrossingToCrossing("E", "Z", 7, False)
g.AddReachableCrossingToCrossing("F", "Z", 11, False)

g.PrintAllCrossingNamesAndReachableCrossings()




