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
                        if direction == Direction.North:
                            direction = Direction.South
                        elif direction == Direction.South:
                            direction = Direction.North
                        elif direction == Direction.West:
                            direction = Direction.East
                        elif direction == Direction.East:
                            direction = Direction.West
                        
                        o.AddReachableCrossing(x, weight, direction)
                        break
                break

    def CalculatePath(self, startDirection, startCrossingName, endCrossingName):
        """
            Kalkuliert den kürzesten Weg von dem eingegebenen Start- und Endpunkt
        """
        for crossing in self.crossings:
            self.unvisited.append(crossing)

        for crossing in self.crossings:
            if(crossing.crossingName == startCrossingName):
                crossing.currentWeight = 0
                crossing.precursor = crossing

                self.CheckIfUturnExists(startDirection, crossing)

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
            for reachableCrossing in crossing.reachableCrossings:
                reachableCrossing.additionalWeight = 0
            self.visited = []
            self.unvisited = []

    
    def CheckIfUturnExists(self, startDirection, startCrossing):
        additionalWeight = 1

        for crossing in startCrossing.reachableCrossings: 
            if startDirection == crossing.direction:
                break

            if startDirection == Direction.North.name and crossing.direction == Direction.South:
                crossing.additionalWeight = additionalWeight
            elif startDirection == Direction.South.name and crossing.direction == Direction.North:
                crossing.additionalWeight = additionalWeight
            elif startDirection == Direction.West.name and crossing.direction == Direction.East:
                crossing.additionalWeight = additionalWeight
            elif startDirection == Direction.East.name and crossing.direction == Direction.West:
                crossing.additionalWeight = additionalWeight

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

            if(reachableCrossing.isLocked == True): 
                continue

            if(self.IsCrossingAlreadyVisited(reachableCrossing)):
                continue

            if reachableCrossing.additionalWeight == 0:
                newWeight = currentCrossing.currentWeight + reachableCrossing.weight
            else:
                newWeight = currentCrossing.currentWeight + reachableCrossing.weight + reachableCrossing.additionalWeight

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
                if(reachableCrossing.crossing == previousCrossing):
                    return True
            return False

    def SetLockForStreet(self, firstCrossing, secondCrossing):
        for crossing in self.crossings:
            if(crossing.crossingName == firstCrossing):
                for reachableCrossing in crossing.reachableCrossings:
                    if(reachableCrossing.crossing.crossingName == secondCrossing):
                        reachableCrossing.isLocked = True
                        return

    def ReleaseLockForStreet(self, firstCrossing, secondCrossing):
        for crossing in self.crossings:
            if(crossing.crossingName == firstCrossing):
                for reachableCrossing in crossing.reachableCrossings:
                    if(reachableCrossing.crossing.crossingName == secondCrossing):
                        reachableCrossing.isLocked = False
                        return
    

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
        self.isLocked = False
        self.crossing = crossing
        self.weight = weight
        self.direction = direction 
        self.additionalWeight = 0

class Direction(enum.Enum):
    North = 1
    East = 2
    South = 3
    West = 4
  


# path = g.CalculatePath("S", "Z")
# print(path)
# path = g.CalculatePath("Z", "S")
# print(path)





