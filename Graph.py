from py_linq import Enumerable
import enum

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
        

    def AddReachableCrossingToCrossing(self, crossingName, neighborCrossingName, weight, isOneWayStreet, direction):
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
                        x.AddReachableCrossing(o, weight, direction)
                        if isOneWayStreet == True: 
                            return
                        o.AddReachableCrossing(x, weight, direction)
                        break
                break

    def CalculatePath(self, startCrossingName, endCrossingName):
        """
            Kalkuliert den kürzesten Weg von dem eingegebenen Start- und Endpunkt
        """
        for crossing in self.crossings:
            self.unvisited.append(crossing)

        for crossing in self.crossings:
            if(crossing.crossingName == startCrossingName):
                crossing.currentWeight = 0
                crossing.precursor = crossing

                self.Dijkstra(crossing)

                path = self.GetPath(endCrossingName)
                path.reverse()

                self.ResetAllCrossingParameterForPathCalculation()

                return path

    def ResetAllCrossingParameterForPathCalculation(self):
        """
            Setzt alle Parameter die für die Berechnung des kürzesten Pfades verwendet werden zurück, sodass
            ein fehlerfreier weiterer Aufruf der Funktion CalculatePath gewährleistet ist.
        """
        for crossing in self.crossings:
            crossing.precursor = None
            crossing.currentWeight = float('inf')
            self.visited = []
            self.unvisited = []
    
    def GetPath(self, crossingName):
        """
            Baut den Pfad vom Start- bis zum Endpunkt mit dem kürzesten weg auf und gibt diesen zurück
            - Rekursiver Aufruf
        """
        for crossing in self.crossings:
            if(crossing.crossingName == crossingName):
                path = []

                if(crossing.crossingName == crossing.precursor.crossingName):
                    return path

                for x in crossing.precursor.reachableCrossings:
                    if(x.crossing == crossing):
                        thisdict = {
                            "currentCrossing": crossing.precursor.crossingName,
                            "direction": x.direction.name,
                            "nextCrossing": x.crossing.crossingName
                        }
                        path.append(thisdict)

                path.extend(self.GetPath(crossing.precursor.crossingName))
                return path                    
    
    def Dijkstra(self, currentCrossing):
        """
            Dijkstra Algorithmus - Rekursiver Aufruf
        """
        for reachableCrossing in currentCrossing.reachableCrossings:

            if(self.IsCrossingAlreadyVisited(reachableCrossing)):
                continue

            newWeight = currentCrossing.currentWeight + reachableCrossing.weight

            if reachableCrossing.crossing.currentWeight == float('inf'):
                reachableCrossing.crossing.currentWeight = newWeight
                reachableCrossing.crossing.precursor = currentCrossing

            elif reachableCrossing.crossing.currentWeight >  newWeight:
                reachableCrossing.crossing.currentWeight = newWeight
                reachableCrossing.crossing.precursor = currentCrossing

        self.visited.append(currentCrossing)
        self.unvisited.remove(currentCrossing)

        minValue = float('inf')
        for reachableCrossing in self.unvisited:
            if(reachableCrossing.currentWeight < minValue):
                minValue = reachableCrossing.currentWeight
                nextCrossing = reachableCrossing

        if len(self.unvisited) != 0:
            self.Dijkstra(nextCrossing)

    def IsCrossingAlreadyVisited(self, reachableCrossing):
        """
            Prüft ob Kreuzung vom Dijkstra Algorithmus bereits abgearbeitet wurde.
        """
        if self.visited != None:
            for previousCrossing in self.visited:
                if(reachableCrossing.crossing.crossingName == previousCrossing):
                    return True
            return False
    

class Crossing:
    def __init__(self, crossingName):
        self.crossingName = crossingName
        self.reachableCrossings = []
        self.currentWeight = float('inf')
        self.precursor = None

    def AddReachableCrossing(self, crossing, weight, direction):
        # check if neighbor already exists
        for x in self.reachableCrossings:
            if(x.crossing == crossing):
                return
        # add neighbor to crossing
        self.reachableCrossings.append(ReachableCrossing(crossing, weight, direction))
    
    def PrintReachableCrossings(self):
        print('\tBenachbart Kreuzungen:', end=" ")
        print(Enumerable(self.reachableCrossings).select(lambda x: x.crossing.crossingName))


class ReachableCrossing:
    def __init__(self, crossing, weight, direction):
        self.crossing = crossing
        self.weight = weight
        self.direction = direction 

class Direction(enum.Enum):
    TurnLeft = 1
    TurnRight = 2
    GoStraight = 3
  
# Main

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

g.AddReachableCrossingToCrossing("S", "A", 5, False, Direction.TurnLeft)
g.AddReachableCrossingToCrossing("S", "B", 2, False, Direction.GoStraight)
g.AddReachableCrossingToCrossing("S", "G", 4, False, Direction.TurnRight)

g.AddReachableCrossingToCrossing("A", "B", 1, False, Direction.TurnRight)
g.AddReachableCrossingToCrossing("A", "C", 3, False, Direction.TurnLeft)

g.AddReachableCrossingToCrossing("B", "C", 8, False, Direction.GoStraight)

g.AddReachableCrossingToCrossing("G", "D", 2, False, Direction.TurnRight)

g.AddReachableCrossingToCrossing("C", "D", 4, False, Direction.TurnLeft)
g.AddReachableCrossingToCrossing("C", "E", 6, False, Direction.GoStraight)

g.AddReachableCrossingToCrossing("D", "E", 10, False, Direction.TurnRight)
g.AddReachableCrossingToCrossing("D", "F", 8, False, Direction.TurnLeft)

g.AddReachableCrossingToCrossing("E", "Z", 7, False, Direction.GoStraight)
g.AddReachableCrossingToCrossing("F", "Z", 11, False, Direction.TurnRight)

g.PrintAllCrossingNamesAndReachableCrossings()

path = g.CalculatePath("S", "Z")
print(path)
path = g.CalculatePath("Z", "S")
print(path)





