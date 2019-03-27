class MapTile:
    def __init__(self,i,j,type):
        print(i)
        self.i_=i
        self.j_=j
        self.type_=type

    def getCoords(self):
        return self.i_,self.j_
    def getType(self):
        return self.type_
    def getX(self):
        return self.i_
    def getY(self):
        return self.j_

    def toString(self):
        return "i: "+ str(self.i_ )+"j: "+str(self.j_)+"type: "+str(self.type_)