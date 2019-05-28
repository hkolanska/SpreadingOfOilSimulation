import math


class MapTile:
    def __init__(self, i, j, type):
        self.i_ = i
        self.j_ = j
        self.type_ = type
        self.oilDensity_ = 0
        self.oilThickness_ = 0
        self.neighbours = []

        self.mass_ = self.oilDensity_ * self.oilThickness_

    def getCoords(self):
        return self.i_, self.j_

    def getType(self):
        return self.type_

    def getX(self):
        return self.i_

    def getY(self):
        return self.j_

    def getMass(self):
        return self.mass_

    def getNeighbours(self):
        return self.neighbours

    def getOilThickness_(self):
        return self.oilThickness_

    def setNeighbours(self, neighbours):
        for n in range(len(neighbours)):
            self.neighbours.append([neighbours[n], 1])

    def setOilDensity(self, newOilDensity):
        self.oilDensity_ = newOilDensity
        self.mass_ = self.oilDensity_ * self.oilThickness_

    def setOilThickness(self, newOilThickness):
        self.oilThickness_ = newOilThickness
        self.mass_ = self.oilDensity_ * self.oilThickness_

    def addNeighbour(self):
        self.neigbours.add

    def addOil(self, oilMass, oilDensity):
        self.mass_ = oilMass + self.mass_
        self.oilDensity_ = oilDensity
        self.oilThickness_ = self.mass_ / self.oilDensity_

    def distance(self, tile):
        x1, y1 = self.getCoords()
        x2, y2 = tile.getCoords()
        du = x2 - x1
        dv = (y2 + x2 // 2) - (y1 + x1 // 2)
        return max(abs(du), abs(dv)) if ((du >= 0 and dv >= 0) or (du < 0 and dv < 0)) else abs(du) + abs(dv)


        #distance = (abs(self.getY() - tile.getY())+abs(self.getX() - tile.getX()))/2
        #return distance

    def toString(self):
        return "i: " + str(self.i_) + "j: " + str(self.j_) + "type: " + str(self.type_) + "maas: " + str(
            self.mass_) + "density: " + str(self.oilDensity_) + "thickness: " + str(self.oilThickness_)

    def setSpreadingRate(self, initialTile, actualTile, theBiggestDistance):
        distance = actualTile.distance(initialTile)
        if distance == 0:
            return theBiggestDistance
        elif (distance < theBiggestDistance):
            return (theBiggestDistance - distance) * 30
        else:
            return 1

    def doMove(self, theBiggestDistance, initialTile):
        m = self.getMass()
        neighbours = self.getNeighbours()
        oilChanges = []
        for i in self.neighbours:
            i[1] = i[1] - 1 + self.setSpreadingRate(initialTile, i[0], theBiggestDistance)
            deltaM = self.deltaMInNaturalSpreading(self, i[0], i[1])
            if deltaM < self.oilDensity_ * theBiggestDistance*1.4:
                oilChanges.append(0)
            else:
                oilChanges.append(deltaM)
        if m < sum(oilChanges):
            deltaM = m / len(neighbours) + 1
            for i in neighbours:
                i[0].addOil(deltaM, self.oilDensity_)
        else:
            for i in range(len(neighbours) - 1):
                if oilChanges[i] != 0:
                    neighbours[i][0].addOil(oilChanges[i], self.oilDensity_)
        return neighbours

    def deltaMInNaturalSpreading(self, tile1, tile2, spreadingRate):
        D = 1 / 27000 * spreadingRate
        return (tile1.getMass() - tile2.getMass()) / 2 * 1 - (math.exp(-2 * D / 2))
