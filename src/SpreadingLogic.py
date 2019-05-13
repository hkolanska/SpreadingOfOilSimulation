import math
from src import MapTile
class SpreadingLogic:
    def __init__(self,map):
        self.oilInitDencity_= 835 #kg/m^3
        self.map_=map
        self.hexWithOilList_=[]
        self.a=5 #m
        self.area_=3*math.sqrt(3)*pow(self.a,2)/2 #m^2

    def deltaMInNaturalSpreading(self,tile1, tile2):
        return tile1.getMass-tile2.getMass

    def change(self,tile):
        m = tile.getMass
        neighbours = tile.getNeighbours
        oilChanges =[]
        for i in neighbours:
            deltaM = self.deltaMInNaturalSpreading(tile,i)
            oilChanges.append(deltaM)
        if m<sum(oilChanges):
            deltaM = m/(neighbours+1)
            for i in neighbours:
                i.addOil(deltaM)
        else:
            for i in range (len(neighbours)-1):
                neighbours[i].addOil(oilChanges[i])




