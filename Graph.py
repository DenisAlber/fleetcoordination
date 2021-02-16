from py_linq import Enumerable

class Graph:
    crossings = []
    visited = []
    unvisited = []
        
    def AddCrossing(self, crossingName):
        self.crossings.append(Crossing(crossingName))

    def PrintAllCrossingNamesAndReachableCrossings(self):
        for x in self.crossings:
            print("Kreuzung: " + x.crossingName)
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

    def CalculatePath(self, StartCrossingName, EndCrossingName):
        for crossing in self.crossings:
            self.unvisited.append(crossing)

        for crossing in self.crossings:
            if(crossing.crossingName == StartCrossingName):
                crossing.currentWeight = 0
                crossing.precursor = crossing
                self.Dijkstra(crossing)
                path = self.GetPath(EndCrossingName)
                path.reverse()
                return path
        


    def GetPath(self, crossingName):
        for crossing in self.crossings:
            if(crossing.crossingName == crossingName):
                path = []
                path.extend(crossing.crossingName)

                if(crossing.crossingName == crossing.precursor.crossingName):
                    return path
                
                path.extend(self.GetPath(crossing.precursor.crossingName))
                return path                    
    
    def Dijkstra(self, currentCrossing):
        path = []
        for reachablecrossing in currentCrossing.reachableCrossings:

            if(self.IsCrossingAlreadyVisited(reachablecrossing)):
                continue

            newWeight = currentCrossing.currentWeight + reachablecrossing.weight

            if reachablecrossing.crossing.currentWeight == float('inf'):
                reachablecrossing.crossing.currentWeight = newWeight
                reachablecrossing.crossing.precursor = currentCrossing

            elif reachablecrossing.crossing.currentWeight >  newWeight:
                reachablecrossing.crossing.currentWeight = newWeight
                reachablecrossing.crossing.precursor = currentCrossing

#            elif reachablecrossing.crossing.currentWeight <  newWeight:
#               continue
        self.visited.append(currentCrossing)
        self.unvisited.remove(currentCrossing)

        minValue = float('inf')
        for reachablecrossing in self.unvisited:

            #if(self.IsCrossingAlreadyVisited(reachablecrossing)):
            #   continue

            if(reachablecrossing.currentWeight < minValue):
                minValue = reachablecrossing.currentWeight
                nextCrossing = reachablecrossing

        if len(self.unvisited) != 0:
            self.Dijkstra(nextCrossing)

    def IsCrossingAlreadyVisited(self, reachablecrossing):
        if self.visited != None:
            for previousCrossing in self.visited:
                if(reachablecrossing.crossing.crossingName == previousCrossing):
                    return True
            return False
            





class Crossing:
    def __init__(self, crossingName):
        self.crossingName = crossingName
        self.reachableCrossings = []
        self.currentWeight = float('inf')
        self.precursor = None

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

path = g.CalculatePath("S", "Z")
print(path)




