import math
class MapTile:
    def __init__(self,i,j,type):
        self.i_=i
        self.j_=j
        self.type_=type
        self.oilDensity_=0
        self.oilThickness_=0
        self.neighbours = []

        self.mass_ = self.oilDensity_ * self.oilThickness_



    def getCoords(self):
        return self.i_,self.j_
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
    def setNeighbours(self,neighbours):
        for n in range (len(neighbours)):
            self.neighbours.append([neighbours[n],1])

    def setOilDensity(self,newOilDensity):
        self.oilDensity_=newOilDensity
        self.mass_ = self.oilDensity_ * self.oilThickness_

    def setOilThickness(self,newOilThickness):
        self.oilThickness_=newOilThickness
        self.mass_ = self.oilDensity_ * self.oilThickness_


    def addNeighbour(self):
        self.neigbours.add

    def addOil(self,oilMass,oilDensity):
        self.mass_=oilMass+self.mass_
        self.oilDensity_=oilDensity
        self.oilThickness_=self.mass_/self.oilDensity_




    def toString(self):
        return "i: "+ str(self.i_ )+"j: "+str(self.j_)+"type: "+str(self.type_)+"maas: "+ str(self.mass_)+"density: "+ str(self.oilDensity_)+"thickness: "+ str(self.oilThickness_)

    def setSpreadingRate(self,startTileX,startTileY,theBiggestDistance):
        return



    def doMove(self):
        m = self.getMass()
        neighbours = self.getNeighbours()
        oilChanges = []
        for i in self.neighbours:
            deltaM = self.deltaMInNaturalSpreading(self, i[0])
            oilChanges.append(deltaM)
        if m < sum(oilChanges):
            deltaM = m / len(neighbours)+1
            for i in neighbours:
                i[0].addOil(deltaM,self.oilDensity_)
                print(deltaM)
        else:
            for i in range(len(neighbours) - 1):
                neighbours[i][0].addOil(oilChanges[i],self.oilDensity_)
        return neighbours

    def deltaMInNaturalSpreading(self,tile1, tile2):
        D=2
        return (tile1.getMass()-tile2.getMass())/2*1-(math.exp(-2*D/2))