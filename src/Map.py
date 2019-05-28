import cv2
import math
import numpy
from src import MapTile


class Map:
    def __init__(self):
        self.listOfMapTiles = []
        img = cv2.imread('..\PNGs\gulfMapGimpBWCurrent.png')
        self.xSize = 902
        self.ySize = 693
        a = 10
        self.xSizeMap = int((self.xSize - a * math.sqrt(3) / 2) / (a * math.sqrt(3)))
        self.ySizeMap = int(self.ySize / (3 * a)*2)
        for i in range(self.xSizeMap):
            lineMapTiles=[]
            for j in range(self.ySizeMap):
                mapTile=self.createTile(i, j, a, img)
                lineMapTiles.append(mapTile)
            self.listOfMapTiles.append(lineMapTiles)
        self.createNeighbourhood()



    def getXSizeMap(self):
        return self.xSizeMap
    def getYSizeMap(self):
        return self.ySizeMap
    def getListOfMapTiles(self):
        return self.listOfMapTiles
    def getTile(self,i,j):
        return self.listOfMapTiles[i][j]

    def createTile(self,x,y,a,img):
        if y % 2 == 0:
            startX = 1.5 * a + a * math.sqrt(3) * x
        else:
            startX = 1.5 * a + a * math.sqrt(3) / 2 + a * math.sqrt(3) * x
        startY = 1.5 * a + 1 / 2 * a + 1.5 * y * a
        angle = 60
        coords = []
        for i in range(1, 7):
            coords.append([int(startX), int(startY)])
            endX = startX + a * math.sin(math.radians(angle * i))
            endY = startY + a * math.cos(math.radians(angle * i))
            startX = endX
            startY = endY
        water=0
        land=0
        type=-1
        for k in coords:
            if k[1]>=self.ySize:
                continue
            if k[0]>=self.xSize:
                continue
            b, g, r = img[k[0]][k[1]]
            if (b==255 and g==255 and r==255):
                water+=1
            else:
                if (r==255 and g==0 and b==0):
                    type=2
                else:
                    land+=1
        if type==-1:
            if land<water:
                type=1
            else:
                type=0
        return MapTile.MapTile(x,y,type)

    def createNeighbourhood(self):
        for i in range(2,self.xSizeMap-2):
            for j in range(2,self.ySizeMap-2):
                self.setNeighbours(self.listOfMapTiles[i][j])

    def getNeighboursByCoords(self, x, y):
        return self.getTile(x, y).getNeighbours()

    def getNeighbours(self, tile):
        return tile.getNeighbours()


    def setNeighbours(self, tile):
        x = tile.getX()
        y = tile.getY()
        neighbours = []
        if y % 2 == 0:
            if x > 0:
                neighbours.append(self.getTile(x - 1, y))
                if y > 0: neighbours.append(self.getTile(x - 1, y - 1))
                if y < self.ySize - 1: neighbours.append(self.getTile(x - 1, y + 1))
            if x < self.xSize - 1: neighbours.append(self.getTile(x + 1, y))
            if y > 0: neighbours.append(self.getTile(x, y - 1))
            if y < self.ySize - 1: neighbours.append(self.getTile(x, y + 1))
            if x > 1 and y > 0: neighbours.append(self.getTile(x-2,y-1))
            if x > 1 and y <self.ySize-1: neighbours.append(self.getTile(x-2,y+1))
            if y > 1: neighbours.append(self.getTile(x,y-2))
            if y < self.ySize-2: neighbours.append(self.getTile(x,y+2))
            if x < self.xSize -1  and y >0: neighbours.append(self.getTile(x+1,y-1))
            if x < self.xSize -1 and y <self.ySize-1:
                neighbours.append(self.getTile(x+1,y+1))

        else:
            if x > 0: neighbours.append(self.getTile(x - 1, y))
            if y > 0: neighbours.append(self.getTile(x, y - 1))
            if y < self.ySize - 1: neighbours.append(self.getTile(x, y + 1))
            if x < self.xSize - 1:
                neighbours.append(self.getTile(x + 1, y))
                if y > 0: neighbours.append(self.getTile(x + 1, y - 1))
                if y < self.ySize - 1: neighbours.append(self.getTile(x + 1, y + 1))
            if x > 0 and y > 0: neighbours.append(self.getTile(x-1,y-1))
            if x > 0 and y <self.ySize-1: neighbours.append(self.getTile(x-1,y+1))
            if y > 1: neighbours.append(self.getTile(x,y-2))
            if y < self.ySize - 4 : neighbours.append(self.getTile(x,y+2))
            if x < self.xSize - 32  and y >1: neighbours.append(self.getTile(x+2,y-1))
            if x < self.xSize -2 and y <self.ySize-1: neighbours.append(self.getTile(x+2,y+1))
        tile.setNeighbours(neighbours)
