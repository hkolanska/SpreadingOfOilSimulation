import cv2
import math
from src import MapTile


class Map:
    def __init__(self):
        self.listOfMapTiles = []
        img = cv2.imread('..\PNGs\mapFragment.png')
        self.xSize = 539
        self.ySize = 337
        self.a= 1.5
        self.xSizeMap = int((self.xSize - self.a* math.sqrt(3) / 2) / (self.a* math.sqrt(3)))
        self.ySizeMap = int(self.ySize / (3 * self.a)*2)
        for i in range(self.xSizeMap):
            lineMapTiles=[]
            for j in range(self.ySizeMap):
                mapTile=self.createTile(i, j, self.a, img)
                lineMapTiles.append(mapTile)
            self.listOfMapTiles.append(lineMapTiles)
        self.createNeighbourhood()
        self.addCurrents(img)
        self.createWind()

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
            startX = 1.5 * self.a+ self.a* math.sqrt(3) * x
        else:
            startX = 1.5 * self.a+ self.a* math.sqrt(3) / 2 + self.a* math.sqrt(3) * x
        startY = 1.5 * self.a+ 1 / 2 * self.a+ 1.5 * y * a
        angle = 60
        coords = []
        for i in range(1, 7):
            coords.append([int(startX), int(startY)])
            endX = startX + self.a* math.sin(math.radians(angle * i))
            endY = startY + self.a* math.cos(math.radians(angle * i))
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
                land+=1
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

    def createWind(self):
        for i in range(2,self.xSizeMap-2):
            for j in range(2,self.ySizeMap-2):
                self.listOfMapTiles[i][j].neighbours[1][1]=200
                self.listOfMapTiles[i][j].neighbours[4][1]=30
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

    def addCurrents(self,img):
        for i in range(2,self.xSizeMap-2):
            for j in range(2,self.ySizeMap-2):
                self.setCurrentValue(self.listOfMapTiles[i][j],img)

    def setCurrentValue(self,tile,img):
        if tile.type_==1:
            return
        x, y = tile.getCoords()
        if y % 2 == 0:
            startX = 1.5 * self.a+ self.a* math.sqrt(3) * x
        else:
            startX = 1.5 * self.a+ self.a* math.sqrt(3) / 2 + self.a* math.sqrt(3) * x
        startY = 1.5 * self.a+ 1 / 2 * self.a+ 1.5 * y * self.a
        angle = 60
        coords = []
        for i in range(1, 7):
            coords.append([int(startX), int(startY)])
            endX = startX + self.a* math.sin(math.radians(angle * i))
            endY = startY + self.a* math.cos(math.radians(angle * i))
            startX = endX
            startY = endY

        for k in coords:
            if k[1]>=self.ySize:
                continue
            if k[0]>=self.xSize:
                continue
            r, g, b = img[k[0]][k[1]]
            if(r==0 and b==0 and g==0) or (r==255 and b==255 and g==255):
                continue
            if (b==0 and g==0 and r==254):
                tile.setSpreadingRateCurrents(0,300)
            if (b==254 and g==0 and r==254):
                tile.setSpreadingRateCurrents(1,300)
            if (b == 254 and g == 254 and r == 0):
                tile.setSpreadingRateCurrents(2,300)
            if (b==98 and g==19 and r==98):
                tile.setSpreadingRateCurrents(3,300)
            if (b==254 and g==0 and r==0):
                tile.setSpreadingRateCurrents(4,300)
            if (b==0 and g==0 and r==254):
                tile.setSpreadingRateCurrents(5,300)

