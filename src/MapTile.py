import math


class MapTile:
    def __init__(self, i, j, type):
        self.i_ = i
        self.j_ = j
        self.type_ = type
        self.oilDensity_ = 0
        self.oilThickness_ = 0
        self.neighbours = []
        self.almostSpreaded=0
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

    def removeOil(self,newOilMass):
        self.mass_ = newOilMass
        self.oilThickness_ = self.mass_ / self.oilDensity_

    def setOilThickness(self, newOilThickness):
        self.oilThickness_ = newOilThickness
        self.mass_ = self.oilDensity_ * self.oilThickness_

    def addNeighbour(self):
        self.neigbours.add

    def addOil(self, oilMass, oilDensity):
        self.mass_ += oilMass
        self.oilDensity_ = oilDensity
        self.oilThickness_ = self.mass_ / self.oilDensity_

    def addAlmostSpreaded(self,value):
        self.almostSpreaded+=value

    def distance(self, tile):
        distance = (abs(self.getY() - tile.getY())+abs(self.getX() - tile.getX()))/2
        return distance

    def toString(self):
        return "i: " + str(self.i_) + "j: " + str(self.j_) + "type: " + str(self.type_) + "maas: " + str(
            self.mass_) + "density: " + str(self.oilDensity_) + "thickness: " + str(self.oilThickness_)

    def setSpreadingRate(self, initialTile, actualTile, theBiggestDistance):
        distance = actualTile.distance(initialTile)
        # if (distance < theBiggestDistance and distance>0):
        #     return theBiggestDistance - distance * 30
        # else:
        return 1

    def setSpreadingRateCurrents(self,num,val):
        self.neighbours[num][1]=val
    def doMove(self, theBiggestDistance, initialTile):

        m = self.getMass()
        neighbours = self.getNeighbours()
        oilChanges = []
        oilToRemove=0
        for i in self.neighbours:
            i[1] = i[1] - 1 + self.setSpreadingRate(initialTile, i[0], theBiggestDistance)
            deltaM = self.deltaMInNaturalSpreading( i[0], i[1])
            if deltaM<0:
                deltaM=0
            if i[0].getMass()<=0:
                if deltaM +i[0].almostSpreaded< self.oilDensity_ *0.003:
                    oilToRemove+=deltaM
                    i[0].addAlmostSpreaded(deltaM)
                    neighbours.remove(i)
                else:
                    oilChanges.append(deltaM + i[0].almostSpreaded)
                    i[0].almostSpreaded = 0
            else:
                oilChanges.append(deltaM)
        if m < sum(oilChanges):
            deltaM = m / (len(neighbours) + 1)
            for i in neighbours:
                i[0].addOil(deltaM, self.oilDensity_)
        else:
            for j in range(len(oilChanges)):
                neighbours[j][0].addOil(oilChanges[j], self.oilDensity_)

        self.removeOil(self.getMass()-sum(oilChanges)-oilToRemove)
        return neighbours

    def deltaMInNaturalSpreading(self, tile2, spreadingRate):
        D = 1 / 27*spreadingRate
        return (self.getMass() - tile2.getMass()) / 2 * (1 - (math.exp(-2 * D / 2)))
